'use strict';

const http = require('node:http');
const { handleRequest } = require('./http/routes.cjs');
const { sendJson } = require('./http/json.cjs');

const PORT = Number(process.env.PORT || 3001);

const server = http.createServer((request, response) => {
  void handleRequest(request, response).catch((error) => {
    if (!response.headersSent) {
      sendJson(response, 500, {
        detail: error instanceof Error ? error.message : String(error),
      });
    } else {
      response.destroy();
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Showdown engine listening on ${PORT}`);
});
