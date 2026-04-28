<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\ContractsController;

Route::prefix('contracts')->group(function () {
    Route::get('/', [ContractsController::class, 'index']);
    Route::get('/{id}', [ContractsController::class, 'show']);
});