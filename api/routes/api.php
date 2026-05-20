<?php

use App\Http\Controllers\ContractsController;
use App\Http\Controllers\EntidadeController;
use App\Http\Controllers\AnalyticsController;
use Illuminate\Support\Facades\Route;

Route::prefix('contracts')->group(function () {
    Route::get('/', [ContractsController::class, 'index']);
    Route::get('/getFilters', [ContractsController::class, 'getFilters']);
    Route::get('/{id}', [ContractsController::class, 'show']);

});

Route::prefix('entidades')->group(function () {
    Route::get('/', [EntidadeController::class, 'index']);
    Route::get('/{id}', [EntidadeController::class, 'show']);
    Route::get('/{id}/listContratcs', [EntidadeController::class, 'listaContratos']);
});

Route::prefix('analytics')->group(function () {

    Route::get('/biggest-contracts', [AnalyticsController::class, 'biggestContracts']);
    Route::get('/smallest-contracts', [AnalyticsController::class, 'smallestContracts']);
    Route::get('/entitiesCompeteMoreEarnLess', [AnalyticsController::class, 'entitiesCompeteMoreEarnLess']);
    Route::get('/entitiesMoreContractsAsContracting', [AnalyticsController::class, 'entitiesMoreContractsAsContracting']);
    Route::get('/search-cpv', [AnalyticsController::class, 'searchCPV']);

});
