'use strict';

const { getOrStartSession, getSession, removeSession } = require('./session_store.cjs');

async function startBattle(input) {
  const session = getOrStartSession(input);
  await session.waitUntilComplete();
  return session.snapshot();
}

function getBattle(battleId) {
  const session = getSession(battleId);
  return session ? session.snapshot() : null;
}

function getBattleSession(battleId) {
  return getSession(battleId);
}

function endBattle(battleId) {
  return removeSession(battleId);
}

async function submitBattleChoice(session, choice) {
  if (session.winner !== null) {
    const error = new Error('Battle is already complete.');
    error.statusCode = 409;
    throw error;
  }

  try {
    return await session.submitChoice(choice);
  } catch (error) {
    const wrapped = new Error(error instanceof Error ? error.message : String(error));
    wrapped.statusCode = session.engineError ? 503 : 422;
    throw wrapped;
  }
}

module.exports = {
  endBattle,
  getBattle,
  getBattleSession,
  startBattle,
  submitBattleChoice,
};
