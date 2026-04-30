<?php

use App\Http\Controllers\ContractsController;
use App\Http\Controllers\EntidadeController;
use Illuminate\Support\Facades\Route;

Route::prefix('contracts')->group(function () {
    Route::get('/', [ContractsController::class, 'index']);
    Route::get('/{id}', [ContractsController::class, 'show']);
});

Route::prefix('entidades')->group(function () {
    Route::get('/', [EntidadeController::class, 'index']);
    Route::get('/{id}', [EntidadeController::class, 'show']);
    Route::get('/{id}/listContratcs', [EntidadeController::class, 'listaContratos']);
});
