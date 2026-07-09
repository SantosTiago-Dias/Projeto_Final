<?php

namespace App\Models;

use App\Http\Resources\TipoProcedimentoResource;
use Illuminate\Database\Eloquent\Model;

class TipoProcedimento extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_tipo_procedimento';
    protected $primaryKey = 'chave_tipo_procedimento';
    public $timestamps = false;
}
