const fs = require('node:fs');
const crypto = require('node:crypto');
const { Dex, TeamValidator } = require('pokemon-showdown');

const format = process.argv[2] || 'gen9nationaldexag';

function normalizeStats(stats) {
  return {
    hp: stats.hp,
    atk: stats.attack,
    def: stats.defense,
    spa: stats['special-attack'],
    spd: stats['special-defense'],
    spe: stats.speed,
  };
}

function validateOne(validator, row) {
  const build = row.build;
  const set = {
    species: row.form_name ? `${row.name}-${row.form_name}` : row.name,
    item: build.held_item || '',
    ability: build.ability,
    moves: build.moves,
    nature: build.nature,
    evs: normalizeStats(build.evs),
    ivs: normalizeStats(build.ivs),
    level: 100,
  };

  try {
    let errors = validator.validateTeam([structuredClone(set)]) || [];
    let finalSet = set;
    if (errors.length) {
      // PokeAPI's version-group lists can include moves that Showdown considers
      // incompatible with the selected format. Repair those candidates from
      // Showdown's own learnset, then validate each set with TeamValidator.
      const speciesName = row.form_name ? `${row.name}-${row.form_name}` : row.name;
      const species = validator.dex.species.get(speciesName);
      const learnsetDex = species.gen < 9 ? Dex.forGen(8) : validator.dex;
      const learnsetSpecies = learnsetDex.species.get(speciesName);
      const movePool = learnsetSpecies.exists
        ? [...learnsetDex.species.getMovePool(learnsetSpecies.id)].sort()
        : [];
      const abilities = Object.values(learnsetSpecies.abilities || {}).filter(Boolean);
      const choices = new Set([build.ability, ...abilities]);
      if (species.exists && movePool.length && abilities.length) {
        const seed = crypto.createHash('sha256').update(row.name).digest('hex');
        let state = Number.parseInt(seed.slice(0, 8), 16) || 1;
        const random = () => {
          state = (1664525 * state + 1013904223) >>> 0;
          return state / 0x100000000;
        };
        const attempts = Math.min(80, Math.max(1, movePool.length * abilities.length));
        for (const ability of choices) {
          for (let attempt = 0; attempt < attempts; attempt += 1) {
            const shuffled = [...movePool];
            for (let i = shuffled.length - 1; i > 0; i -= 1) {
              const j = Math.floor(random() * (i + 1));
              [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            const candidate = {
              ...set,
              ability,
              moves: shuffled.slice(0, Math.min(4, shuffled.length)),
            };
            const candidateErrors = validator.validateTeam([structuredClone(candidate)]) || [];
            if (!candidateErrors.length) {
              finalSet = candidate;
              errors = [];
              break;
            }
            errors = candidateErrors;
          }
          if (!errors.length) break;
        }
      }
      if (errors.length && species.exists && movePool.length && abilities.length) {
        for (const ability of choices) {
          const repaired = { ...set, ability, moves: [] };
          for (const move of movePool) {
            if (repaired.moves.length === 4) break;
            const candidate = { ...repaired, moves: [...repaired.moves, move] };
            const candidateErrors = validator.validateTeam([structuredClone(candidate)]) || [];
            if (!candidateErrors.length) repaired.moves.push(move);
          }
          if (repaired.moves.length) {
            finalSet = repaired;
            errors = [];
            break;
          }
        }
      }
    }
    return {
      pokemon_id: row.pokemon_id,
      name: row.name,
      valid: errors.length === 0,
      errors,
      repaired_build: errors.length === 0 ? {
        ability: finalSet.ability,
        moves: finalSet.moves,
      } : null,
    };
  } catch (error) {
    return {
      pokemon_id: row.pokemon_id,
      name: row.name,
      valid: false,
      errors: [error instanceof Error ? error.message : String(error)],
    };
  }
}

try {
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  if (!Array.isArray(input)) throw new Error('Input must be a JSON array.');
  const validator = new TeamValidator(format);
  const results = input.map((row) => validateOne(validator, row));
  process.stdout.write(JSON.stringify({ format, results }));
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
}
