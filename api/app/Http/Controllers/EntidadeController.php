<?php

namespace App\Http\Controllers;

use App\Filters\EntidadeFilter;
use App\Http\Requests\EntidadeFilterRequest;
use App\Http\Resources\EntidadeResource;
use App\Http\Resources\ListContractsResource;
use App\Models\DimDetalhesContrato;
use App\Models\DimEntidade;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;

class EntidadeController extends Controller
{
    public function index(EntidadeFilterRequest $request)
    {
        try {
            $cachedIds = Cache::rememberForever('entidades:list', function () {
                return DimEntidade::where('id_entidade', '!=', -1)
                    ->pluck('id_entidade')
                    ->toArray();
            });

            $entidades = DimEntidade::whereIn('id_entidade', $cachedIds)->paginate(25);

            return EntidadeResource::collection($entidades);

        } catch (\Throwable $e) {
            abort(500, 'Error: ' . $e->getMessage());
        }
    }

    public function show($id)
    {
        if ($id == -1)
        {
            abort(404, 'Not Found');
        }

        #TODO:ISTO DEVE DE HAVER UMA MANEIRA MELHOR DE FAZER
        $cacheKey = 'entidades:show:' . $id;

        if (Cache::has($cacheKey))
        {
            return response()->json(Cache::get($cacheKey));
        }
        else
        {
            $entidade =DimEntidade::find($id);

            if (is_null($entidade))
            {
                abort(404, 'Not Found');
            }
        }

        $data = new EntidadeResource($entidade);
        Cache::put($cacheKey, json_decode($data->toJson(),true), now()->addDay(1));

        return response()->json($data);
    }

    public function listaContratos($id)
    {
        if ($id == -1) {
            abort(404, 'Entidade não encontrada');
        }

        $entidadeCacheKey = 'entidade:show:' . $id;

        $entidadeData = Cache::rememberForever($entidadeCacheKey, function () use ($id) {
            return DimEntidade::where('chave_entidade', $id)
                ->first()
                ?->toArray();
        });

        if (!$entidadeData) {
            abort(404, 'Entidade não encontrada');
        }

        $contractIdsCacheKey = 'entidade:contratos:ids:' . $id;

        $cachedIds = Cache::rememberForever($contractIdsCacheKey, function () use ($entidadeData) {
            return DimDetalhesContrato::whereHas('fact_contrato', function ($query) use ($entidadeData) {
                $query->where('adjudicante', $entidadeData['chave_entidade'])
                ->orWhere('chave_entidade', $entidadeData['chave_entidade']);
            })
                ->pluck('chave_contratos')
                ->toArray();
        });

        // Rebuild query from IDs with full relations for pagination
        $contratos = DimDetalhesContrato::with([
            'cpvs',
            'fact_contrato.entidade',
            'fact_contrato.tipo_contrato',
            'fact_contrato.tipo_procedimento',
            'fact_contrato.data',
            'fact_contrato.concorrentes',
        ])
            ->whereIn('chave_contratos', $cachedIds)
            ->paginate(25);

        return ListContractsResource::collection($contratos);
    }
}
