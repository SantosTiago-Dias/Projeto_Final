<?php

namespace App\Models;

use App\Http\Resources\TipoContratoResource;
use App\Http\Resources\TipoProcedimentoResource;
use Illuminate\Database\Eloquent\Model;

class TipoContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_tipo_contrato';
    protected $primaryKey = 'chave_tipo_contrato';
    public $timestamps = false;
}
