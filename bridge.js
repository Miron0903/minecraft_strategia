const mineflayer = require('mineflayer');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

let bot = null;
let botConnected = false;

// Функция для подключения бота к серверу
function connectBot(host, port, username) {
    if (bot) {
        bot.end();
    }

    bot = mineflayer.createBot({
        host: host,
        port: port,
        username: username
    });

    bot.on('login', () => {
        console.log(`✅ Бот ${username} подключился к ${host}:${port}`);
        botConnected = true;
    });

    bot.on('error', (err) => {
        console.log('❌ Ошибка бота:', err);
    });

    bot.on('end', () => {
        console.log('🔌 Бот отключился');
        botConnected = false;
    });

    bot.on('chat', (username, message) => {
        console.log(`💬 ${username}: ${message}`);
    });

    return { status: 'connecting', username: username };
}

// API для управления ботом из Python
app.post('/connect', (req, res) => {
    const { host, port, username } = req.body;
    const result = connectBot(host, port, username);
    res.json(result);
});

app.post('/move', (req, res) => {
    const { direction, steps } = req.body;

    if (!bot || !botConnected) {
        return res.json({ error: 'Бот не подключен' });
    }

    console.log(`🚶 Движение: ${direction} на ${steps} шагов`);

    // Двигаемся плавно
    for (let i = 0; i < steps; i++) {
        setTimeout(() => {
            if (bot && botConnected) {
                bot.setControlState(direction, true);
                setTimeout(() => {
                    if (bot && botConnected) {
                        bot.setControlState(direction, false);
                    }
                }, 300);
            }
        }, i * 400);
    }

    res.json({ status: 'moving', direction, steps });
});

app.post('/jump', (req, res) => {
    if (!bot || !botConnected) {
        return res.json({ error: 'Бот не подключен' });
    }

    console.log('🦘 Прыжок!');
    bot.setControlState('jump', true);
    setTimeout(() => {
        if (bot) bot.setControlState('jump', false);
    }, 500);

    res.json({ status: 'jumped' });
});

app.post('/chat', (req, res) => {
    const { message } = req.body;

    if (!bot || !botConnected) {
        return res.json({ error: 'Бот не подключен' });
    }

    console.log(`💬 Бот говорит: ${message}`);
    bot.chat(message);
    res.json({ status: 'message sent', message });
});

app.get('/position', (req, res) => {
    if (!bot || !botConnected) {
        return res.json({ error: 'Бот не подключен' });
    }

    try {
        const pos = bot.entity.position;
        // Отправляем всегда валидные числа
        res.json({
            x: Math.round(pos.x * 10) / 10,
            y: Math.round(pos.y * 10) / 10,
            z: Math.round(pos.z * 10) / 10
        });
    } catch (e) {
        res.json({
            error: 'Cannot get position',
            x: 0,
            y: 0,
            z: 0
        });
    }
});

app.post('/disconnect', (req, res) => {
    if (bot) {
        bot.end();
        bot = null;
        botConnected = false;
    }
    console.log('🔌 Отключаем бота');
    res.json({ status: 'disconnected' });
});

// Запускаем сервер для Python
const PORT = 3000;
app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🚀 МОСТ ЗАПУЩЕН!');
    console.log(`🌐 Порт: ${PORT}`);
    console.log('📡 Жду команды из Python...');
    console.log('='.repeat(50));
});