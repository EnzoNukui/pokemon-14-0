'use strict';

const { RandomPlayerAI } = require('pokemon-showdown/dist/sim/tools/random-player-ai');

function startRandomOpponent(stream, session, signal) {
  const ai = new RandomPlayerAI(stream);
  void ai.start().catch((error) => {
    session.engineError = error instanceof Error ? error.message : String(error);
    signal();
  });
}

module.exports = { startRandomOpponent };
