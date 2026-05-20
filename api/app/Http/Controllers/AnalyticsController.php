<?php

namespace App\Http\Controllers;
use App\Models\ViewEntitiesCompeteMoreEarnLess;
use App\Models\ViewEntitiesMoreContractsAsContracting;
use App\Models\ViewSmallestContracts;
use Illuminate\Http\Request;
use App\Models\ViewBiggestContracts;
use Illuminate\Support\Facades\DB;

class AnalyticsController extends Controller
{
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
}
