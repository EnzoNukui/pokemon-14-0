'use strict';

const { BattleSession } = require('./battle_session.cjs');

const sessions = new Map();

function getSession(battleId) {
  return sessions.get(battleId) || null;
}

function getOrStartSession(input) {
  const existing = getSession(input.battle_id);
  if (existing) return existing;

  const session = new BattleSession(input);
  sessions.set(input.battle_id, session);
  return session;
}

function removeSession(battleId) {
  const session = sessions.get(battleId);
  if (!session) return null;
  sessions.delete(battleId);
  session.close();
  return session;
}

module.exports = { getOrStartSession, getSession, removeSession };
