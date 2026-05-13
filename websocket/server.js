const redis = require('redis');

const REDIS_SERVER = "redis://:TESTE@redis:6379";
const channel = 'ETL';
const redisClient = redis.createClient({ url: REDIS_SERVER });

redisClient.on('error', (err) => console.error('Redis error:', err));


redisClient.connect().then(r => {
    console.log(`Connected to ${REDIS_SERVER}:${channel}`);
});

redisClient.subscribe(channel, (message) => {
    const data = JSON.parse(message);

    console.log(data);

    if (data?.status === 'end') {
        console.log('ETL finished! Message: ' + data.message);

        // your equivalent of Cache::flush() + broadcast here
        console.log('Send broadcast');
    }
});