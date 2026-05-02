<?php

namespace App\Http\Controllers;

use App\Http\Resources\DetailsContractResource;
use App\Http\Resources\ListContractsResource;
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
                'fact_contrato.concorrentes'
            ])->where('chave_contratos','!=',1)->paginate(25);

            //TODO:FILTROS

            return ListContractsResource::collection($contratos);

        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function show($id)
    {

        try
        {
            if ($id == -1)
            {
                abort(404);
            }

            $contrato = DimDetalhesContrato::with([
                'fact_contrato.entidade',
                'fact_contrato.tipo_contrato',
                'fact_contrato.tipo_procedimento',
                'fact_contrato.data',
                'fact_contrato.concorrentes',
                'cpvs'])->where('chave_contratos', $id)
                ->first();

            if (!$contrato) {
                abort(404);
            }

            return new DetailsContractResource($contrato);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }

    }
}
