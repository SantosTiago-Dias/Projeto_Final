<?php

namespace App\Http\Controllers;
use App\Models\DimDetalhesContrato;
use App\Models\FactContrato;
use App\Models\ViewEntitiesCompeteMoreEarnLess;
use App\Models\ViewEntitiesMoreContractsAsContracting;
use App\Models\ViewSmallestContracts;
use Illuminate\Http\Request;
use App\Models\ViewBiggestContracts;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

class AnalyticsController extends Controller
{
    public function biggestContracts()
    {
        $cacheKey = 'biggestContracts';
        $contracts = Cache::rememberForever($cacheKey, function () {
            return ViewBiggestContracts::select("*")
                ->get()
                ->toArray();
        });
        return response()->json($contracts);
    }

    public function smallestContracts()
    {
        $cacheKey = 'smallestContracts';
        $contracts = Cache::rememberForever($cacheKey, function () {
            return ViewSmallestContracts::select("*")
                ->get()
                ->toArray();
        });

        return response()->json($contracts);
    }

    public function entitiesCompeteMoreEarnLess()
    {
        $cacheKey = 'entitiesCompeteMoreEarnLess';
        $contracts = Cache::rememberForever($cacheKey, function () {
            return ViewEntitiesCompeteMoreEarnLess::select("*")
                ->get()
                ->toArray();
        });

        return response()->json($contracts);
    }

    public function entitiesMoreContractsAsContracting()
    {
        $cacheKey = 'entitiesMoreContractsAsContracting';
        $contracts = Cache::rememberForever($cacheKey, function () {
            return ViewEntitiesMoreContractsAsContracting::select("*")
                ->get()
                ->toArray();
        });

        return response()->json($contracts);
    }

    public function searchCPV(Request $request)
    {

        $input = $request->input('query');
        $cacheKey = 'searchCPV'.$input;


        $result = Cache::rememberForever($cacheKey,function () use ($input) {
            return DB::select('CALL search_cpv(?)', [$input]);
        });

        return response()->json($result[0] ?? null);
    }

    public function tipoContrato()
    {
        $cacheKey = 'tipoContrato:graphdata';
        $tipo_contratos = Cache::rememberForever($cacheKey, function () {
            return FactContrato::with(['tipo_contrato'])
                ->whereNot('chave_tipo_contrato', 1)
                ->whereNot('chave_contratos', 1)
                ->select('chave_tipo_contrato', DB::raw('count(DISTINCT chave_contratos) as contratos'))
                ->groupBy('chave_tipo_contrato')
                ->get()
                ->toArray();
        });


        return response()->json($tipo_contratos);

    }

    public function tipoProcedimento()
    {
        $cacheKey = 'tipoProcedimento:graphdata';
        $tipo_procedimento = Cache::rememberForever($cacheKey,function () {
            return FactContrato::with(['tipo_procedimento'])
                ->whereNot('chave_tipo_procedimento', 1)
                ->whereNot('chave_contratos', 1)
                ->select('chave_tipo_procedimento', DB::raw('count(DISTINCT chave_contratos) as contratos'))
                ->groupBy('chave_tipo_procedimento')
                ->get()
                ->toArray();
        });

        return response()->json($tipo_procedimento);

    }
}
