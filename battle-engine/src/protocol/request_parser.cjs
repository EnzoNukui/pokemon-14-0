'use strict';

function applyPlayerRequestLine(line, session) {
  if (line.startsWith('|request|')) {
    try {
      session.request = JSON.parse(line.slice('|request|'.length));
      session.requestCount += 1;
    } catch {
      session.engineError = 'Showdown returned an invalid player request.';
    }
  } else if (line.startsWith('|error|')) {
    session.lastChoiceError = line.slice('|error|'.length);
  }
}

module.exports = { applyPlayerRequestLine };
