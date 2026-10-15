'use strict';

const MAX_BODY_BYTES = 1024 * 1024;

function sendJson(response, status, value) {
  response.writeHead(status, { 'content-type': 'application/json' });
  response.end(JSON.stringify(value));
}

async function readJson(request) {
  let body = '';
  for await (const chunk of request) {
    body += chunk;
    if (Buffer.byteLength(body) > MAX_BODY_BYTES) {
      throw new Error('Request body is too large.');
    }
  }
  return body ? JSON.parse(body) : {};
}

module.exports = { readJson, sendJson };
