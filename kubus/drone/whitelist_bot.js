const mineflayer = require('mineflayer')
const { mineflayer: mineflayerViewer } = require('prismarine-viewer')

const bot = mineflayer.createBot({
    host: 'localhost',
    username: 'Bot',
    version: '1.19'
})

bot.on('login', () => {
    mineflayerViewer(bot, {port: 3007, firstPerson: false})
    window.open('http://localhost:3007')
})