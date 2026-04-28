<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TipoContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'tipo_contrato_dictionary';
    protected $primaryKey = 'id_tipo_contrato';
    public $timestamps = false;
}
