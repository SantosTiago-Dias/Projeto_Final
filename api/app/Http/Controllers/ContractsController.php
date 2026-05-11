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
        try {
            $request->validated();

            $cacheKey = 'contracts:list';
            $fromCache = Cache::has($cacheKey);

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

            return [
                'from_cache' => $fromCache,
                'data'       => ListContractsResource::collection($result),
            ];

        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function show($id)
    {

        try {
            if ($id == -1) {
                abort(404);
            }

            $cacheKey = 'contract:show:' . $id;

            $contratoArray = Cache::rememberForever($cacheKey, function () use ($id) {
                $contrato = DimDetalhesContrato::with([
                    'fact_contrato.entidade',
                    'fact_contrato.tipo_contrato',
                    'fact_contrato.tipo_procedimento',
                    'fact_contrato.data',
                    'fact_contrato.concorrentes',
                    'cpvs',
                ])->where('chave_contratos', $id)->first();

                return $contrato?->toArray(); // ✅ full data, fully serializable
            });

            if (!$contratoArray) {
                abort(404);
            }

            return response()->json([
                'from_cache' => Cache::has($cacheKey),
                'data'       => $contratoArray, // ✅ return directly, no Resource needed
            ]);

        } catch (\Throwable $e) {
            abort(500, 'Error: ' . $e->getMessage());
        }

    }

    public function getFilters(): JsonResponse
    {
        $tipoContratoCacheKey    = 'tipo_contrato:list';
        $tipoProcedimentoCacheKey = 'tipo_procedimento:list';

        // Cache only IDs
        $tipoContratoIds = Cache::rememberForever($tipoContratoCacheKey, function () {
            return TipoContrato::where('id_tipo_contrato', '!=', 1)
                ->pluck('id_tipo_contrato')
                ->toArray();
        });

        $tipoProcedimentoIds = Cache::rememberForever($tipoProcedimentoCacheKey, function () {
            return TipoProcedimento::where('id_tipo_procedimento', '!=', 1)
                ->pluck('id_tipo_procedimento')
                ->toArray();
        });

        // Rebuild collections from IDs
        $tipoContrato     = TipoContrato::whereIn('id_tipo_contrato', $tipoContratoIds)->get();
        $tipoProcedimento = TipoProcedimento::whereIn('id_tipo_procedimento', $tipoProcedimentoIds)->get();

        return response()->json([
            'TipoContrato'     => TipoContratoResource::collection($tipoContrato),
            'TipoProcedimento' => TipoProcedimentoResource::collection($tipoProcedimento),
        ]);
    }
}
