'use strict';

const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const http = require('node:http');
const { after, before, test } = require('node:test');
const { handleRequest } = require('../src/http/routes.cjs');
const { isSupportedChoice } = require('../src/http/validation.cjs');
const { normalizeEvent } = require('../src/protocol/event_parser.cjs');

let server;
let baseUrl;

function createPokemon(species, ability, moves) {
  return {
    species,
    ability,
    moves,
    nature: 'Serious',
    evs: { hp: 4, atk: 252, spe: 252 },
    ivs: { hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31 },
    level: 100,
  };
}

function createTeam() {
  return [
    createPokemon('Pikachu', 'Static', ['Thunderbolt', 'Quick Attack', 'Iron Tail', 'Protect']),
    createPokemon('Charizard', 'Blaze', ['Flamethrower', 'Air Slash', 'Roost', 'Dragon Claw']),
    createPokemon('Blastoise', 'Torrent', ['Surf', 'Ice Beam', 'Rapid Spin', 'Protect']),
    createPokemon('Venusaur', 'Overgrow', ['Giga Drain', 'Sludge Bomb', 'Sleep Powder', 'Synthesis']),
    createPokemon('Snorlax', 'Thick Fat', ['Body Slam', 'Crunch', 'Rest', 'Sleep Talk']),
    createPokemon('Gengar', 'Cursed Body', ['Shadow Ball', 'Sludge Bomb', 'Focus Blast', 'Destiny Bond']),
  ];
}

before(async () => {
  server = http.createServer((request, response) => {
    void handleRequest(request, response).catch((error) => {
      if (!response.headersSent) {
        response.writeHead(500, { 'content-type': 'application/json' });
        response.end(JSON.stringify({ detail: error.message }));
      } else {
        response.destroy();
      }
    });
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  baseUrl = `http://127.0.0.1:${address.port}`;
});

after(async () => {
  server.closeAllConnections();
  await new Promise((resolve, reject) =>
    server.close((error) => error ? reject(error) : resolve()),
  );
});

test('choice validation accepts supported moves and rejects malformed commands', () => {
  assert.equal(isSupportedChoice('move 1'), true);
  assert.equal(isSupportedChoice('move 4 mega'), true);
  assert.equal(isSupportedChoice('switch 6'), true);
  assert.equal(isSupportedChoice('team 123456'), true);
  assert.equal(isSupportedChoice('move 5'), false);
  assert.equal(isSupportedChoice('switch 7'), false);
  assert.equal(isSupportedChoice('move 1; exit'), false);
  assert.equal(isSupportedChoice(null), false);
});

test('Showdown event lines normalize for live client responses', () => {
  assert.deepEqual(normalizeEvent('|move|p1a: Pikachu|Thunderbolt|p2a: Snorlax'), {
    event_type: 'move',
    payload: {
      parts: ['p1a: Pikachu', 'Thunderbolt', 'p2a: Snorlax'],
      line: '|move|p1a: Pikachu|Thunderbolt|p2a: Snorlax',
    },
  });
});

test('HTTP service starts a Showdown battle, accepts a turn, returns state, and closes it', { timeout: 45000 }, async () => {
  const battleId = `node-integration-${randomUUID()}`;

  const health = await fetch(`${baseUrl}/health`);
  assert.equal(health.status, 200);
  assert.equal((await health.json()).status, 'ok');

  const start = await fetch(`${baseUrl}/battles`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      battle_id: battleId,
      format: 'gen7anythinggoes',
      player: { name: 'Player', team: createTeam() },
      opponent: { name: 'Trainer', team: createTeam() },
    }),
  });
  assert.equal(start.status, 201, await start.clone().text());
  const initialState = await start.json();
  assert.equal(initialState.status, 'RUNNING');
  assert.ok(initialState.request);
  assert.ok(initialState.engine_version);
  assert.ok(Array.isArray(initialState.events));

  let currentState = initialState;
  if (currentState.request.teamPreview) {
    const preview = await fetch(`${baseUrl}/battles/${battleId}/choices`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ choice: 'team 123456' }),
    });
    assert.equal(preview.status, 200, await preview.clone().text());
    currentState = await preview.json();
  }

  const availableMoves = currentState.request.active[0].moves;
  const firstUsableMove = availableMoves.findIndex((move) => !move.disabled && move.pp > 0);
  assert.notEqual(firstUsableMove, -1, 'Showdown should expose at least one available move');
  const choice = `move ${firstUsableMove + 1}`;

  const turn = await fetch(`${baseUrl}/battles/${battleId}/choices`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ choice }),
  });
  assert.equal(turn.status, 200, await turn.clone().text());
  const turnState = await turn.json();
  assert.ok(['RUNNING', 'COMPLETED'].includes(turnState.status));
  assert.ok(Array.isArray(turnState.events));

  const current = await fetch(`${baseUrl}/battles/${battleId}`);
  assert.equal(current.status, 200);
  assert.ok(['RUNNING', 'COMPLETED'].includes((await current.json()).status));

  const removed = await fetch(`${baseUrl}/battles/${battleId}`, { method: 'DELETE' });
  assert.equal(removed.status, 204);
  const missing = await fetch(`${baseUrl}/battles/${battleId}`);
  assert.equal(missing.status, 404);
});
