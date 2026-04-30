<?php

use App\Http\Controllers\EntidadeController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\ContractsController;

Route::prefix('contracts')->group(function () {
    Route::get('/', [ContractsController::class, 'index']);
    Route::get('/{id}', [ContractsController::class, 'show']);
});

Route::prefix('entidades')->group(function () {
    Route::get('/', [EntidadeController::class, 'index']);
    Route::get('/{id}', [EntidadeController::class, 'show']);
});
