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
use Illuminate\Support\Facades\Cache;

class ContractsController extends Controller
{
    public function index(ContratoFilterRequest $request)
    {
        $request->validated();

        $cacheKey = 'contracts:list';

        //Load all data to Cache
        $contratos = Cache::rememberForever($cacheKey, function () {
            return DimDetalhesContrato::where('chave_contratos', '!=', 1)
                ->pluck('chave_contratos')
                ->toArray();
        });

        // Rebuild query from cached IDs so filters
        $query = DimDetalhesContrato::with([
            'cpvs',
            'fact_contrato.entidade',
            'fact_contrato.tipo_contrato',
            'fact_contrato.tipo_procedimento',
            'fact_contrato.data',
            'fact_contrato.concorrentes',
        ])->whereIn('chave_contratos', $contratos);

        $result = ContratoFilter::apply($query, $request->validated())->paginate(25);

        return ListContractsResource::collection($result);
    }

    public function show($id)
    {
        if ($id == 1)
        {
            abort(404,'Contrato não encontrado');
        }

        $cacheKey = 'contract:show:' . $id;

        if (Cache::has($cacheKey))
        {
            return response()->json(Cache::get($cacheKey));
        }
        else
        {
            $contrato = DimDetalhesContrato::with([
                'fact_contrato.entidade',
                'fact_contrato.tipo_contrato',
                'fact_contrato.tipo_procedimento',
                'fact_contrato.data',
                'fact_contrato.concorrentes',
                'cpvs',
            ])->find($id);

            if (is_null($contrato))
            {
                abort(404, 'Not Found');
            }

            $data = new DetailsContractResource($contrato);


            Cache::put($cacheKey, json_decode($data->toJson(),true), now()->addHours(1));

            return response()->json($data);
        }
    }

    public function getFilters(): JsonResponse
    {
        $tipoContratoCacheKey    = 'tipo_contrato:list';
        $tipoProcedimentoCacheKey = 'tipo_procedimento:list';

        // Cache only IDs
        $tipoContratoIds = Cache::rememberForever($tipoContratoCacheKey, function () {
            return TipoContrato::where('chave_tipo_contrato', '!=', 1)
                ->pluck('chave_tipo_contrato')
                ->toArray();
        });

        $tipoProcedimentoIds = Cache::rememberForever($tipoProcedimentoCacheKey, function () {
            return TipoProcedimento::where('chave_tipo_procedimento', '!=', 1)
                ->pluck('chave_tipo_procedimento')
                ->toArray();
        });

        // Rebuild collections from IDs
        $tipoContrato     = TipoContrato::whereIn('chave_tipo_contrato', $tipoContratoIds)->get();
        $tipoProcedimento = TipoProcedimento::whereIn('chave_tipo_procedimento', $tipoProcedimentoIds)->get();

        return response()->json([
            'TipoContrato'     => TipoContratoResource::collection($tipoContrato),
            'TipoProcedimento' => TipoProcedimentoResource::collection($tipoProcedimento),
        ]);
    }

    public function numberContracts(): JsonResponse
    {
        $cacheKey = 'contracts:numberOfCountracs';

        $numberContracts = Cache::rememberForever($cacheKey, function () {
            return DimDetalhesContrato::all()->count();
        });

        return response()->json([
            'numberContracts' => $numberContracts
        ]);


    }
}
