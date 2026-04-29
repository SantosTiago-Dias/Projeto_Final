<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\ContractsResource;
use App\Http\Resources\FactsResource;
use App\Models\FactContrato;
use Illuminate\Http\Request;

class ContractsController extends Controller
{
    //TODO:sql Injection
    public function index(Request $request)
    {
        try {

            $data=FactContrato::with('contrato.cpvs.cpv','contrato','entidade','concorrentes','tipo_contrato','tipo_procedimento','data')->paginate(25);

            //TODO:APLICAR FILTROS

            return FactsResource::collection($data);

        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

public function show($id)
{
    $rows = FactContrato::with([
        'contrato.cpvs.cpv',
        'contrato',
        'entidade',
        'adjudicanteRel',
        'tipoContrato',
        'tipoProcedimento',
        'data'
    ])
    ->where('chave_contratos', $id)
    ->get();

    if ($rows->isEmpty()) {
        abort(404);
    }

    return response()->json([
        'contrato' => $rows->first()->contrato,
        'adjudicanteRel' => $rows->first()->adjudicanteRel,
        'tipo_contrato' => $rows->first()->tipoContrato,
        'tipo_procedimento' => $rows->first()->tipoProcedimento,
        'data' => $rows->first()->data,

        'adjudicatario' => $rows->firstWhere('adjudicatario', 1)?->entidade,

        'entidades' => $rows->where('adjudicatario', 0)->map(fn($r) => $r->entidade)->values()

    ]);
}
}
