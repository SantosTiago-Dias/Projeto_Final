const redis = require('redis');
const ws = require('ws');

const SOCKET_PORT = process.env.SOCKET_PORT || 3000;
const REDIS_SERVER = `redis://:${process.env.REDIS_PASSWORD}@${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`;
const channel = process.env.REDIS_CHANNEL;
const redisClient = redis.createClient({ url: REDIS_SERVER });
const server = new ws.Server({ port : SOCKET_PORT });

//try to listen server
redisClient.on('error', (err) => console.error('Redis error:', err));

//try to connect server
redisClient.connect().then(r => {
    console.log(`Connected to ${REDIS_SERVER}:${channel}`);
});

//When ETL is done broadcast the message to frontend
server.on ('connection', (socket) => {
    redisClient.subscribe(channel, (message) => {
        const data = JSON.parse(message);

        console.log(data);

        if (data?.status === 'end') {
            console.log('ETL finished! Message: ' + data.message);

            //broadcast to all users
            server.clients.forEach(client => {
                if (client.readyState === ws.OPEN) {
                    client.send("Novos dados Disponiveis");
                }
            });
        }
    });
})