'use strict';

const { Dex } = require('pokemon-showdown');
const { RandomPlayerAI } = require('pokemon-showdown/dist/sim/tools/random-player-ai');

function toSpecies(details) {
  const speciesName = String(details || '').split(',')[0].trim();
  return speciesName ? Dex.species.get(speciesName) : null;
}

function healthRatio(pokemon) {
  const match = String(pokemon?.condition || '').match(/^(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)/);
  if (!match) return 1;
  const current = Number(match[1]);
  const maximum = Number(match[2]);
  return maximum > 0 ? Math.max(0, Math.min(1, current / maximum)) : 0;
}

function effectiveness(sourceType, targetTypes) {
  if (!sourceType || !targetTypes.length) return 1;
  if (!Dex.getImmunity(sourceType, targetTypes)) return 0;
  return 2 ** Dex.getEffectiveness(sourceType, targetTypes);
}

function scoreMove(candidate, ownTypes, foeTypes, currentHp) {
  const move = Dex.moves.get(candidate.move);
  if (!move.exists) return 1;

  if (move.category === 'Status') {
    if (move.heal && currentHp < 0.6) return 35 + (0.6 - currentHp) * 90;
    if (move.boosts) return currentHp > 0.65 ? 28 : 16;
    if (move.status || move.volatileStatus) return 26;
    if (move.sideCondition || move.weather || move.terrain) return 20;
    return 8;
  }

  const power = candidate.zMove ? Math.max(move.basePower || 0, 120) : move.basePower || 0;
  if (power <= 0) return 35;

  const rawAccuracy = move.accuracy;
  const accuracy = rawAccuracy === true ? 1 : typeof rawAccuracy === 'number' ? rawAccuracy / 100 : 1;
  const stab = ownTypes.includes(move.type) ? 1.5 : 1;
  const typeMultiplier = effectiveness(move.type, foeTypes);
  if (typeMultiplier === 0) return 0;

  let score = power * accuracy * stab * typeMultiplier;
  score += (move.priority || 0) * 8;
  if (move.drain) score += 8;
  if (move.recoil) score -= 6;
  return score;
}

function pokemonScore(pokemon, foeTypes) {
  const species = toSpecies(pokemon?.details);
  if (!species?.types) return 0;

  const hp = healthRatio(pokemon);
  const bestMove = (pokemon.moves || []).reduce((best, moveName) => {
    return Math.max(best, scoreMove({ move: moveName }, species.types, foeTypes, hp));
  }, 0);
  const incomingThreat = foeTypes.length
    ? Math.max(...foeTypes.map((type) => effectiveness(type, species.types)))
    : 1;

  return (bestMove * hp) / Math.max(1, incomingThreat);
}

class StrategicPlayerAI extends RandomPlayerAI {
  constructor(stream, session, side, profile) {
    super(stream, { move: 1, mega: 0 });
    this.session = session;
    this.side = side;
    this.profile = profile;
    this.request = null;
    this.lastSwitchAgainstSpecies = null;
  }

  receiveRequest(request) {
    this.request = request;
    // RandomPlayerAI interprets `move` as the chance to keep attacking. A low
    // value makes it switch almost every turn, so switching is now a deliberate
    // response to a clear matchup problem instead of a random frequent choice.
    this.move = this.shouldSwitch(request) ? 0 : 1;
    super.receiveRequest(request);
  }

  shouldSwitch(request) {
    const active = request.active?.[0];
    const ownPokemon = request.side?.pokemon?.find((pokemon) => pokemon.active);
    if (!active || active.trapped || !ownPokemon) return false;

    const foeSide = this.side === 'p1' ? 'p2' : 'p1';
    const foeSpeciesName = this.session.activeSpecies?.[foeSide];
    const foeSpecies = toSpecies(foeSpeciesName);
    const foeTypes = foeSpecies?.types || [];
    if (!foeTypes.length) return false;

    const alternatives = (request.side.pokemon || [])
      .filter((pokemon) => !pokemon.active && !String(pokemon.condition).endsWith(' fnt'));
    if (!alternatives.length) return false;

    const currentSpecies = toSpecies(ownPokemon.details);
    const currentTypes = currentSpecies?.types || [];
    const currentScore = pokemonScore(ownPokemon, foeTypes);
    const bestBenchScore = Math.max(...alternatives.map((pokemon) => pokemonScore(pokemon, foeTypes)));
    const currentHp = healthRatio(ownPokemon);
    const threat = currentTypes.length
      ? Math.max(...foeTypes.map((type) => effectiveness(type, currentTypes)))
      : 1;
    const bestCurrentMove = (active.moves || [])
      .filter((move) => !move.disabled)
      .reduce((best, move) => Math.max(
        best,
        scoreMove({ move: move.move }, currentTypes, foeTypes, currentHp),
      ), 0);
    const hasStrongHit = bestCurrentMove >= 100;
    const emergency = currentHp <= 0.18;
    const severeMismatch = threat >= 4 && currentHp <= 0.6 && !hasStrongHit;
    const weakenedMismatch = threat >= 2 && currentHp <= 0.32 && !hasStrongHit;

    // Prevent the back-and-forth switching loop: after a tactical switch, stay
    // in against the same opposing Pokémon unless the new active is near fainting.
    if (foeSpeciesName === this.lastSwitchAgainstSpecies && !emergency) return false;

    return bestBenchScore > 0 && (
      (emergency && bestBenchScore >= currentScore * 0.7) ||
      (severeMismatch && bestBenchScore >= currentScore * 1.25) ||
      (weakenedMismatch && bestBenchScore >= currentScore * 1.5)
    );
  }

  chooseMove(active, candidates) {
    const ownPokemon = this.request?.side?.pokemon?.find((pokemon) => pokemon.active);
    const ownSpecies = toSpecies(ownPokemon?.details);
    const ownTypes = ownSpecies?.types || [];
    const foeSide = this.side === 'p1' ? 'p2' : 'p1';
    const foeSpecies = toSpecies(this.session.activeSpecies?.[foeSide]);
    const foeTypes = foeSpecies?.types || [];
    const ownHp = healthRatio(ownPokemon);

    const scored = candidates.map((candidate) => {
      return {
        ...candidate,
        score: scoreMove(candidate.move, ownTypes, foeTypes, ownHp),
      };
    });
    const highest = Math.max(...scored.map((candidate) => candidate.score));
    const bestChoices = scored.filter((candidate) => candidate.score === highest);
    return this.prng.sample(bestChoices).choice;
  }

  chooseSwitch(_active, switches) {
    const foeSide = this.side === 'p1' ? 'p2' : 'p1';
    this.lastSwitchAgainstSpecies = this.session.activeSpecies?.[foeSide] || null;
    const foeSpecies = toSpecies(this.session.activeSpecies?.[foeSide]);
    const foeTypes = foeSpecies?.types || [];
    const ranked = switches
      .map(({ slot, pokemon }) => ({ slot, score: pokemonScore(pokemon, foeTypes) }))
      .sort((left, right) => right.score - left.score);
    return ranked[0]?.slot ?? switches[0].slot;
  }
}

function startStrategicPlayer(stream, session, side, profile) {
  const ai = new StrategicPlayerAI(stream, session, side, profile);
  void ai.start().catch((error) => {
    session.engineError = error instanceof Error ? error.message : String(error);
    session.signal();
  });
}

module.exports = { startStrategicPlayer };
