'use strict';

const { BattleStream, getPlayerStreams } = require('pokemon-showdown');
const { startStrategicPlayer } = require('../ai/strategic_player.cjs');
const { observeBattleLog } = require('./stream_observers.cjs');

function createBattleStreams(input, session) {
  const battle = new BattleStream({ keepAlive: true });
  const streams = getPlayerStreams(battle);
  const signal = () => session.signal();
  const opponentName = String(input.opponent.name || 'Trainer').slice(0, 18);
  const opponentCategory = input.opponent.category || 'CHAMPION';

  startStrategicPlayer(streams.p1, session, 'p1', 'player');
  startStrategicPlayer(streams.p2, session, 'p2', opponentCategory);
  observeBattleLog(streams.omniscient, session, opponentName, signal);

  const player = { name: session.playerName, team: session.teams.player };
  const opponent = { name: opponentName, team: session.teams.opponent };
  void streams.omniscient.write(
    `>start ${JSON.stringify({ formatid: input.format || 'gen9nationaldexag' })}\n` +
    `>player p1 ${JSON.stringify(player)}\n>player p2 ${JSON.stringify(opponent)}`,
  );

  return streams;
}

module.exports = { createBattleStreams };
