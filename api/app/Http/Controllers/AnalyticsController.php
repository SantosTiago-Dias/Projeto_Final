<?php

namespace App\Http\Controllers;
use App\Models\DimDetalhesContrato;
use App\Models\FactContrato;
use App\Models\ViewEntitiesCompeteMoreEarnLess;
use App\Models\ViewEntitiesMoreContractsAsContracting;
use App\Models\ViewSmallestContracts;
use Illuminate\Http\Request;
use App\Models\ViewBiggestContracts;
use Illuminate\Support\Facades\DB;

class AnalyticsController extends Controller
{
    //TODO: Implementar Cache
    public function biggestContracts()
    {
        $contracts = ViewBiggestContracts::select("*")
            ->get()
            ->toArray();
        return response()->json($contracts);
    }

    public function smallestContracts()
    {
        $contracts = ViewSmallestContracts::select("*")
            ->get()
            ->toArray();
        return response()->json($contracts);
    }

    public function entitiesCompeteMoreEarnLess()
    {
        $contracts = ViewEntitiesCompeteMoreEarnLess::select("*")
            ->get()
            ->toArray();
        return response()->json($contracts);
    }

    public function entitiesMoreContractsAsContracting()
    {
        $contracts = ViewEntitiesMoreContractsAsContracting::select("*")
            ->get()
            ->toArray();
        return response()->json($contracts);
    }

    public function searchCPV(Request $request)
    {
        $input = $request->input('query');

        $result = DB::select('CALL search_cpv(?)', [$input]);

        return response()->json($result[0] ?? null);
    }

    public function tipoContrato()
    {
        $tipo_contratos = FactContrato::with(['tipo_contrato'])
            ->whereNot('chave_tipo_contrato', 1)
            ->whereNot('chave_contratos', 1)
            ->select('chave_tipo_contrato', DB::raw('count(DISTINCT chave_contratos) as contratos'))
            ->groupBy('chave_tipo_contrato')
            ->get();

        return response()->json($tipo_contratos);

    }

    public function tipoProcedimento()
    {
        $tipo_contratos = FactContrato::with(['tipo_procedimento'])
            ->whereNot('chave_tipo_procedimento', 1)
            ->whereNot('chave_contratos', 1)
            ->select('chave_tipo_procedimento', DB::raw('count(DISTINCT chave_contratos) as contratos'))
            ->groupBy('chave_tipo_procedimento')
            ->get();

        return response()->json($tipo_contratos);

    }
}
