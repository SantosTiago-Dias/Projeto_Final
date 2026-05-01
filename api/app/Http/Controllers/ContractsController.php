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

            $all = FactContrato::with('contrato.cpvs.cpv', 'contrato', 'entidade', 'concorrentes', 'tipo_contrato', 'tipo_procedimento', 'data')
                ->get()
                ->unique('chave_contratos')
                ->values();
            //TODO:APLICAR FILTROS

            $perPage = 25;
            $page = request()->input('page', 1);

            $contratos = new LengthAwarePaginator(
                $all->forPage($page, $perPage), // items for current page
                $all->count(),                  // total items
                $perPage,
                $page,
                ['path' => request()->url()]    // keeps URL correct
            );

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
