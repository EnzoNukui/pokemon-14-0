'use strict';

const { applyBattleLogLine } = require('../protocol/event_parser.cjs');
const { applyPlayerRequestLine } = require('../protocol/request_parser.cjs');

function messageOf(error) {
  return error instanceof Error ? error.message : String(error);
}

function observeBattleLog(stream, session, opponentName, signal) {
  void (async () => {
    try {
      for await (const chunk of stream) {
        for (const line of chunk.split('\n')) {
          applyBattleLogLine(line, session, opponentName);
        }
        signal();
      }
    } catch (error) {
      session.engineError = messageOf(error);
      signal();
    }
  })();
}

function observePlayerRequests(stream, session, signal) {
  void (async () => {
    try {
      for await (const chunk of stream) {
        for (const line of chunk.split('\n')) {
          applyPlayerRequestLine(line, session);
        }
        signal();
      }
    } catch (error) {
      session.engineError = messageOf(error);
      signal();
    }
  })();
}

module.exports = { observeBattleLog, observePlayerRequests };
