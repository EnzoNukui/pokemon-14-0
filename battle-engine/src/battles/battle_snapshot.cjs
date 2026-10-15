'use strict';

const engineVersion = require('pokemon-showdown/package.json').version;

function snapshot(session) {
  const result = session.winner === null ? null :
    session.winner === 'tie' ? 'DRAW' :
      session.winner === session.playerName ? 'WIN' : 'LOSS';
  const events = session.pendingEvents.splice(0);
  return {
    status: result ? 'COMPLETED' : 'RUNNING',
    request: session.request,
    simulator_result: result,
    engine_version: engineVersion,
    events,
  };
}

module.exports = { snapshot };
