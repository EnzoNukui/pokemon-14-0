'use strict';

const { readJson, sendJson } = require('./json.cjs');
const {
  endBattle,
  getBattle,
  getBattleSession,
  startBattle,
  submitBattleChoice,
} = require('../battles/battle_service.cjs');
const { isSupportedChoice } = require('./validation.cjs');
const engineVersion = require('pokemon-showdown/package.json').version;

async function handleRequest(request, response) {
  const url = new URL(request.url, 'http://127.0.0.1');
  if (request.method === 'GET' && url.pathname === '/health') {
    return sendJson(response, 200, {
      status: 'ok',
      engine: 'pokemon-showdown',
      engine_version: engineVersion,
    });
  }

  if (request.method === 'POST' && url.pathname === '/battles') {
    try {
      const input = await readJson(request);
      return sendJson(response, 201, await startBattle(input));
    } catch (error) {
      return sendJson(response, 422, {
        detail: error instanceof Error ? error.message : String(error),
      });
    }
  }

  const match = url.pathname.match(/^\/battles\/([^/]+)(?:\/choices)?$/);
  if (!match) return sendJson(response, 404, { detail: 'Not found.' });
  const battleId = match[1];
  const session = getBattleSession(battleId);
  if (!session) {
    return sendJson(response, 404, {
      detail: 'Battle session not found in this engine process.',
    });
  }

  if (request.method === 'GET' && !url.pathname.endsWith('/choices')) {
    return sendJson(response, 200, getBattle(battleId));
  }
  if (request.method === 'DELETE' && !url.pathname.endsWith('/choices')) {
    endBattle(battleId);
    response.writeHead(204);
    return response.end();
  }
  if (request.method === 'POST' && url.pathname.endsWith('/choices')) {
    try {
      const { choice } = await readJson(request);
      if (!isSupportedChoice(choice)) {
        return sendJson(response, 422, { detail: 'Unsupported battle choice.' });
      }
      return sendJson(response, 200, await submitBattleChoice(session, choice));
    } catch (error) {
      const status = error.statusCode || (session.engineError ? 503 : 422);
      return sendJson(response, status, {
        detail: error instanceof Error ? error.message : String(error),
      });
    }
  }
  return sendJson(response, 404, { detail: 'Not found.' });
}

module.exports = { handleRequest };
