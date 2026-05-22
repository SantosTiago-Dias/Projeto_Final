<?php

namespace App\Http\Controllers;

use App\Filters\EntidadeFilter;
use App\Http\Requests\EntidadeFilterRequest;
use App\Http\Resources\EntidadeResource;
use App\Http\Resources\ListaContratosEntidadeResource;
use App\Http\Resources\ListContractsResource;
use App\Models\DimDetalhesContrato;
use App\Models\DimEntidade;
use App\Models\FactContrato;
use Illuminate\Http\Request;

class EntidadeController extends Controller
{
    //
    public function index(EntidadeFilterRequest $request)
    {
        try {

            $query = DimEntidade::query()
                ->where('chave_entidade', '!=', -1);

            $query = EntidadeFilter::apply($query, $request->validated());

            $entidades = $query->paginate(25);

            return EntidadeResource::collection($entidades);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function show($id)
    {
        if ($id == -1)
        {
            abort(404, 'Not Found');
        }

        try {
                return DimEntidade::all()->firstOrFail('chave_entidade', $id);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function listaContratos($id)
    {
        $entidade = DimEntidade::where('chave_entidade', $id)->first();

        if (!$entidade ||  $id === 1)
        {
            abort(404, 'Entidade not found');
        }

        $contratos = DimDetalhesContrato::with([
            'cpvs',
            'fact_contrato.entidade',
            'fact_contrato.tipo_contrato',
            'fact_contrato.tipo_procedimento',
            'fact_contrato.data',
            'fact_contrato.concorrentes'
        ])
            ->whereHas('fact_contrato', function ($query) use ($entidade) {
                $query->where('adjudicante', $entidade->chave_entidade)
                    ->orWhere('chave_entidade', $entidade->chave_entidade);
            })
            ->paginate(25);

        return ListContractsResource::collection($contratos);
    }
}
