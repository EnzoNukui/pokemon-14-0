'use strict';

function normalizeEvent(line) {
  const parts = line.split('|');
  return { event_type: parts[1] || 'message', payload: { parts: parts.slice(2), line } };
}

function applyBattleLogLine(line, session, opponentName) {
  if (!line.startsWith('|')) return;

  session.pendingEvents.push(normalizeEvent(line));
  const parts = line.split('|');
  if (parts[1] === 'win') {
    session.winner = parts[2] === session.playerName
      ? session.playerName
      : opponentName;
  }
  if (parts[1] === 'tie') session.winner = 'tie';
}

module.exports = { applyBattleLogLine, normalizeEvent };
