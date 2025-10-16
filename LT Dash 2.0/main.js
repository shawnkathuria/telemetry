//FIRST TIME: `npm install`
//TO RUN: `ts-node main.ts`
const express = require('express');
const app = express();
const ip = require('ip');
const ipAddress = ip.address();

const PORT_TO_WEBSERVER = 4000;

//SERVING WEBSERVER:
app.use(express.json());
app.use(express.static('./public'));

const server = app.listen(PORT_TO_WEBSERVER, () => {
    console.log(`Express WebServer running on ${ipAddress}:${PORT_TO_WEBSERVER}`);
    console.log('Express WebServer listening on port ' + PORT_TO_WEBSERVER);
});

server.on('error', (err) => console.error('Server error:', err));
server.on('close', () => console.log('Server closed'));

process.on('exit', (code) => console.log('Process exit with code:', code));