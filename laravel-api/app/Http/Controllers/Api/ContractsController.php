<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\FactContrato;
use Illuminate\Http\Request;

class ContractsController extends Controller
{
    /*
    public function index(Request $request)
    {
        try {
        $query = FactContrato::with([
            'contrato',
            'entidade',
            'adjudicante',
            'tipoContrato',
            'tipoProcedimento',
            'data'
        ]);

        if ($request->from) {
            $query->whereHas('data', fn($q) =>
                $q->where('data', '>=', $request->from));
        }

        if ($request->to) {
            $query->whereHas('data', fn($q) =>
                $q->where('data', '<=', $request->to));
        }

        if ($request->min_valor) {
            $query->where('valor_contratual', '>=', $request->min_valor);
        }

        if ($request->max_valor) {
            $query->where('valor_contratual', '<=', $request->max_valor);
        }

        return response()->json(
            $query->paginate($request->get('per_page', 50))
        );

    } catch (\Throwable $e) {
        return response()->json([
            'error' => $e->getMessage()
        ], 500);
    }
    }*/

    public function index(Request $request)
    {
        try {

            $query = FactContrato::with([
                'contrato',
                'entidade',
                'adjudicanteRel',
                'tipoContrato',
                'tipoProcedimento',
                'data'
            ]);

            // filtros
            if ($request->from) {
                $query->whereHas('data', fn($q) =>
                    $q->where('data', '>=', $request->from));
            }

            if ($request->to) {
                $query->whereHas('data', fn($q) =>
                    $q->where('data', '<=', $request->to));
            }

            if ($request->min_valor) {
                $query->where('valor_contratual', '>=', $request->min_valor);
            }

            if ($request->max_valor) {
                $query->where('valor_contratual', '<=', $request->max_valor);
            }

            $rows = $query->get();

            // agrupar por contrato
            $grouped = $rows->groupBy('chave_contratos')->map(function ($group) {
                $first = $group->first();

                return [
                    'contrato' => $first->contrato,
                    'adjudicanteRel' => $first->adjudicanteRel,
                    'tipo_contrato' => $first->tipoContrato,
                    'tipo_procedimento' => $first->tipoProcedimento,
                    'data' => $first->data,

                    'entidades' => $group->map(fn($r) => $r->entidade)->values(),

                    'valor_total' => $group->sum('valor_contratual')
                ];
            })->values();

            return response()->json([
                'data' => $grouped
            ]);

        } catch (\Throwable $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

/*
    public function show($id)
    {
        $data = FactContrato::with([
            'contrato',
            'entidade',
            'adjudicante',
            'tipoContrato',
            'tipoProcedimento',
            'data'
        ])->where('chave_contratos', $id)->get();

        return response()->json($data);
    }
*/
public function show($id)
{
    $rows = FactContrato::with([
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

        'entidades' => $rows->map(fn($r) => $r->entidade),

        'valor_total' => $rows->sum('valor_contratual')
    ]);
}
}