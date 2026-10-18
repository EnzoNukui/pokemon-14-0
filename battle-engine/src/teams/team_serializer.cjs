'use strict';

const { Dex, Teams } = require('pokemon-showdown');

const MINIMUM_DAMAGE_MOVES = 3;
const MINIMUM_RELIABLE_MOVES = 2;
const RELIABLE_MOVE_POWER = 60;

function selectUsefulMoves(set) {
  const species = Dex.species.get(set.species || set.name);
  if (!species.exists) return set.moves || [];

  const learnsetDex = species.gen < 9 ? Dex.forGen(8) : Dex.forGen(9);
  const learnsetSpecies = learnsetDex.species.get(species.id);
  if (!learnsetSpecies.exists) return set.moves || [];

  const currentMoves = (set.moves || [])
    .map((name) => learnsetDex.moves.get(name))
    .filter((move) => move.exists);
  const currentDamageMoves = currentMoves.filter((move) => move.basePower > 0);
  const currentReliableMoves = currentDamageMoves.filter((move) => move.basePower >= RELIABLE_MOVE_POWER);
  const hasStab = currentDamageMoves.some((move) => species.types.includes(move.type));
  const needsRepair =
    currentDamageMoves.length < MINIMUM_DAMAGE_MOVES ||
    currentReliableMoves.length < MINIMUM_RELIABLE_MOVES ||
    !hasStab;
  if (!needsRepair) return set.moves;

  const candidates = [...learnsetDex.species.getMovePool(learnsetSpecies.id)]
    .map((id) => learnsetDex.moves.get(id))
    .filter((move) => move.exists && move.basePower > 0 && move.category !== 'Status')
    .map((move) => {
      const accuracy = typeof move.accuracy === 'number' ? move.accuracy : 100;
      const stab = species.types.includes(move.type);
      const isPreferredCategory =
        (move.category === 'Physical' && species.baseStats.atk >= species.baseStats.spa) ||
        (move.category === 'Special' && species.baseStats.spa > species.baseStats.atk);
      return {
        id: move.id,
        type: move.type,
        stab,
        score: move.basePower * (accuracy / 100) + (stab ? 35 : 0) + (isPreferredCategory ? 12 : 0),
      };
    })
    .sort((left, right) => right.score - left.score || left.id.localeCompare(right.id));

  const selected = [];
  const selectedIds = new Set();
  const addBest = (predicate, limit) => {
    for (const move of candidates) {
      if (selected.length >= 4 || limit <= 0) break;
      if (selectedIds.has(move.id) || !predicate(move)) continue;
      selected.push(move.id);
      selectedIds.add(move.id);
      limit -= 1;
    }
  };

  addBest((move) => move.stab, 2);
  addBest((move) => !move.stab, 2);
  addBest(() => true, 4);
  return selected.length ? selected : set.moves || [];
}

function alignGeneratedNature(set) {
  const natureId = Dex.natures.get(set.nature).id;
  if (natureId !== 'adamant' && natureId !== 'modest') return;

  const species = Dex.species.get(set.species || set.name);
  if (!species.exists) return;
  const dex = species.gen < 9 ? Dex.forGen(8) : Dex.forGen(9);
  const powerByCategory = (set.moves || []).reduce((totals, name) => {
    const move = dex.moves.get(name);
    if (move.exists && move.basePower > 0) totals[move.category] += move.basePower;
    return totals;
  }, { Physical: 0, Special: 0 });

  if (powerByCategory.Special > powerByCategory.Physical && natureId === 'adamant') {
    set.nature = 'Modest';
  } else if (powerByCategory.Physical > powerByCategory.Special && natureId === 'modest') {
    set.nature = 'Adamant';
  }
}

function defaultPlayerItem(set) {
  const species = Dex.species.get(set.species || set.name);
  if (!species.exists) return 'Sitrus Berry';

  const { hp, def, spd } = species.baseStats;
  const bulk = hp + Math.round((def + spd) / 2);
  if (bulk >= 190) return 'Leftovers';
  if (species.baseStats.spe >= 100 || species.baseStats.atk >= 120 || species.baseStats.spa >= 120) {
    return 'Shell Bell';
  }
  return 'Sitrus Berry';
}

function preparePlayerSet(set) {
  const prepared = { ...set };
  prepared.moves = selectUsefulMoves(prepared);
  alignGeneratedNature(prepared);
  if (!prepared.item) prepared.item = defaultPlayerItem(prepared);
  return prepared;
}

function serializeTeams(input) {
  if (!input.battle_id || !input.player?.team?.length || !input.opponent?.team?.length) {
    throw new Error('battle_id and both non-empty teams are required.');
  }

  return {
    player: Teams.pack(input.player.team.map(preparePlayerSet)),
    opponent: Teams.pack(
      input.opponent.category === 'CHAMPION_CHALLENGE'
        ? input.opponent.team.map(preparePlayerSet)
        : input.opponent.team,
    ),
  };
}

module.exports = { serializeTeams };
