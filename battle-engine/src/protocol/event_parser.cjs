'use strict';

const { Dex } = require('pokemon-showdown');

function normalizeEvent(line) {
  const parts = line.split('|');
  const payload = { parts: parts.slice(2), line };
  if (parts[1] === 'move') {
    payload.move_type = Dex.moves.get(parts[3]).type;
  }
  return { event_type: parts[1] || 'message', payload };
}

function applyBattleLogLine(line, session, opponentName) {
  if (!line.startsWith('|')) return;

  session.pendingEvents.push(normalizeEvent(line));
  const parts = line.split('|');
  if (parts[1] === 'switch' || parts[1] === 'drag') {
    const side = parts[2]?.match(/^p[12]/)?.[0];
    const species = parts[3]?.split(',')[0]?.trim();
    if (side && species) session.activeSpecies[side] = species;
  }
  if (parts[1] === 'tie') {
    // A tie is the final outcome even if a later protocol line also contains a winner.
    session.winner = 'tie';
  } else if (parts[1] === 'win' && session.winner !== 'tie') {
    session.winner = parts[2] === session.playerName
      ? session.playerName
      : opponentName;
  }
}

module.exports = { applyBattleLogLine, normalizeEvent };
