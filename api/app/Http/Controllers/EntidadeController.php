<?php

namespace App\Http\Controllers;

use App\Http\Resources\EntidadeResource;
use App\Models\DimEntidade;
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

            $entidades = DimEntidade::where('id_entidade', $id)->get();

            if ($entidades->isEmpty())
            {
                abort(404, 'Entidade not found');
            }

            return EntidadeResource::collection($entidades);
        } catch (\Throwable $e) {
            abort(500, 'Error'. $e->getMessage());
        }
    }
}
