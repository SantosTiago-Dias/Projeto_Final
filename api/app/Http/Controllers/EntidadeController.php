<?php

namespace App\Http\Controllers;

use App\Http\Resources\EntidadeResource;
use App\Http\Resources\ListaContratosEntidadeResource;
use App\Models\DimDetalhesContrato;
use App\Models\DimEntidade;
use App\Models\FactContrato;
use Illuminate\Http\Request;

class EntidadeController extends Controller
{
    //
    public function index()
    {
        try {

            $entidades = DimEntidade::where('id_entidade', '!=', -1)->paginate(25);

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
                return DimEntidade::all()->firstOrFail('id_entidade', $id);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }

    public function listaContratos($id)
    {
        $entidade = DimEntidade::where('id_entidade', $id)->first();

        if (!$entidade ||  $id === 1)
        {
            abort(404, 'Entidade not found');
        }

        $contratos = DimDetalhesContrato::with([
            'fact_contrato.entidade',
            'fact_contrato.tipo_contrato',
            'fact_contrato.tipo_procedimento',
            'fact_contrato.data',
            'fact_contrato.concorrentes'
        ])->where('adjudicante',$entidade->chave_entidade)->orWhere('chave_entidade',$entidade->chave_entidade)->paginate(25);

        return ListaContratosEntidadeResource::collection($contratos);
    }
}
