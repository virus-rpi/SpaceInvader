const { Client } = require('mineflyer');

function checkWhitelist(serverAddress, serverPort) {
  const client = new Client();

  client.on('connect', () => {
    client.handshake(serverAddress, serverPort);
    client.loginStart('YourBotUsername');
  });

  client.on('playerListHeaderFooter', ({ header }) => {
    if (header === '§fThere are §b0 §fof a max of §b20 §fplayers online:') {
      console.log('The server does not have a whitelist enabled.');
    } else {
      console.log('The server has a whitelist enabled.');
    }

    client.disconnect();
  });

  client.connect(serverAddress, serverPort);
}

// Replace 'serverAddress' and 'serverPort' with the actual server details
checkWhitelist('serverAddress', serverPort);
