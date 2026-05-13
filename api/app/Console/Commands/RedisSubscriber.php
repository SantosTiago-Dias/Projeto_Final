<?php

namespace App\Console\Commands;

use App\Events\NewDataAvailable;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Redis;

#[Signature('redis:subscribe {channel=ETL}')]
#[Description('Subscribe to a Redis Pub/Sub channel')]

class RedisSubscriber extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        $channel = $this->argument('channel');
        $this->info("Subscribing to channel: {$channel}");

        Redis::subscribe([$channel], function (string $message, string $channel) {
            $data = json_decode($message, true);
            $this->line($data);
            if (isset($data['status']) && $data['status'] === 'end') {
                // handle success
                $this->line("ETL finished! Message: " . $data['message']);

                Cache::flush();
                $this->line("Send broadcast");

                broadcast(new NewDataAvailable([
                    'message' => 'New data is ready',
                    'timestamp' => now()->toISOString(),
                ]))->toOthers();
            }
        });
    }
}
