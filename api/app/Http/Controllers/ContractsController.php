<?php

namespace App\Http\Controllers;

use App\Http\Resources\FactsResource;
use App\Models\FactContrato;

class ContractsController extends Controller
{
    public function index()
    {
        try {

            $contratos=FactContrato::with('contrato.cpvs.cpv','contrato','entidade','concorrentes','tipo_contrato','tipo_procedimento','data')->paginate(25);

            //TODO:APLICAR FILTROS

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
