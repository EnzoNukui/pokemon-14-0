const fs = require('node:fs');
const { Dex } = require('pokemon-showdown');

const rows = JSON.parse(fs.readFileSync(0, 'utf8'));
if (!Array.isArray(rows)) throw new Error('Input must be a JSON array.');

const dex = Dex.forFormat('gen9nationaldexag');
const results = rows.map((row) => {
  const species = dex.species.get(row.name);
  return {
    pokemon_id: row.pokemon_id,
    name: row.name,
    exists: species.exists,
    competitive_tier: species.exists ? species.tier : null,
    source_format: 'gen9nationaldexag',
    is_nonstandard: species.exists ? species.isNonstandard || null : null,
  };
});

process.stdout.write(JSON.stringify({ generation: 9, results }));
