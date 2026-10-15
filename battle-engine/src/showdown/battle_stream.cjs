'use strict';

const { BattleStream, getPlayerStreams } = require('pokemon-showdown');
const { startRandomOpponent } = require('../ai/random_opponent.cjs');
const { observeBattleLog, observePlayerRequests } = require('./stream_observers.cjs');

function createBattleStreams(input, session) {
  const battle = new BattleStream({ keepAlive: true });
  const streams = getPlayerStreams(battle);
  const signal = () => session.signal();
  const opponentName = String(input.opponent.name || 'Trainer').slice(0, 18);

  startRandomOpponent(streams.p2, session, signal);
  observeBattleLog(streams.omniscient, session, opponentName, signal);
  observePlayerRequests(streams.p1, session, signal);

  const player = { name: session.playerName, team: session.teams.player };
  const opponent = { name: opponentName, team: session.teams.opponent };
  void streams.omniscient.write(
    `>start ${JSON.stringify({ formatid: input.format || 'gen9nationaldexag' })}\n` +
    `>player p1 ${JSON.stringify(player)}\n>player p2 ${JSON.stringify(opponent)}`,
  );

  return streams;
}

module.exports = { createBattleStreams };
