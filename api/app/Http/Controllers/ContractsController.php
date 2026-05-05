<?php

namespace App\Http\Controllers;

use App\Filters\ContratoFilter;
use App\Http\Requests\ContratoFilterRequest;
use App\Http\Resources\DetailsContractResource;
use App\Http\Resources\ListContractsResource;
use App\Http\Resources\TipoContratoResource;
use App\Http\Resources\TipoProcedimentoResource;
use App\Models\DimDetalhesContrato;
use App\Models\TipoContrato;
use App\Models\TipoProcedimento;
use Illuminate\Http\JsonResponse;

class ContractsController extends Controller
{
    public function index(ContratoFilterRequest $request)
    {
        try {
            $request->validated();
            $query = DimDetalhesContrato::with(['cpvs','fact_contrato.entidade','fact_contrato.tipo_contrato','fact_contrato.tipo_procedimento','fact_contrato.data','fact_contrato.concorrentes'])->where('chave_contratos','!=',1);

            //TODO:FILTROS
            $contratos = ContratoFilter::apply($query, $request->validated())->paginate(25);

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

    public function getFilters(): JsonResponse
    {
        return response()->json([
            'TipoContrato' => TipoContratoResource::collection(
                TipoContrato::where('id_tipo_contrato', '!=', 1)->get()
            ),
            'TipoProcedimento' => TipoProcedimentoResource::collection(
                TipoProcedimento::where('id_tipo_procedimento', '!=', 1)->get()
            ),
        ]);
    }
}
