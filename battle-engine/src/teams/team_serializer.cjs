'use strict';

const { Teams } = require('pokemon-showdown');

function serializeTeams(input) {
  if (!input.battle_id || !input.player?.team?.length || !input.opponent?.team?.length) {
    throw new Error('battle_id and both non-empty teams are required.');
  }

  return {
    player: Teams.pack(input.player.team),
    opponent: Teams.pack(input.opponent.team),
  };
}

module.exports = { serializeTeams };
