<?php

namespace App\Http\Controllers;

use App\Http\Resources\FactsResource;
use App\Models\DimDetalhesContrato;
use App\Models\FactContrato;
use Illuminate\Pagination\LengthAwarePaginator;

class ContractsController extends Controller
{
    public function index()
    {
        try {
            $contratos = DimDetalhesContrato::with([
                'fact_contrato.entidade',
                'fact_contrato.tipo_contrato',
                'fact_contrato.tipo_procedimento',
                'fact_contrato.data',
                'fact_contrato.concorrentes',
            ])->where('chave_contratos','!=',1)->paginate(25);

            //TODO:FILTROS

            return FactsResource::collection($contratos);

        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function show($id)
    {
        try
        {
            $data = FactContrato::with('contrato.cpvs.cpv','contrato','entidade','concorrentes','tipo_contrato','tipo_procedimento','data')
                ->where('chave_contratos', $id)
                ->first();

            if (!$data) {
                abort(404);
            }

            return new FactsResource($data);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }

    }
}
