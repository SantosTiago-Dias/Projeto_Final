const redis = require('redis');
const ws = require('ws');

const SOCKET_PORT = process.env.SOCKET_PORT || 3000;
const REDIS_SERVER = `redis://:${process.env.REDIS_PASSWORD}@${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`;
const channel = process.env.REDIS_CHANNEL;

const redisClient = redis.createClient({ url: REDIS_SERVER });
const server = new ws.Server({ port: SOCKET_PORT });

//Broadcast message to all users connected
function broadcast(message) {
    server.clients.forEach(client => {
        if (client.readyState === ws.OPEN) {
            client.send(message);
        }
    });
}

//On error
redisClient.on('error', (err) => console.error('Redis error:', err));

//Redis connect to channel
redisClient.connect().then(() => {
    console.log(`Connected to Redis, listening on channel: ${channel}`);

    redisClient.subscribe(channel, (message) => {
        const data = JSON.parse(message);
        console.log('Received:', data);

        if (data?.status === 'end') {
            broadcast('Novos dados Disponíveis');
        }
    });
});

server.on('connection', (socket) => {
    console.log('WS client connected');
    socket.on('close', () => console.log('WS client disconnected'));
});