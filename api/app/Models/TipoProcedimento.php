<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TipoProcedimento extends Model
{
    protected $connection = 'etl';
    protected $table = 'tipo_procedimento_dictionary';
    protected $primaryKey = 'id_tipo_procedimento';
    public $timestamps = false;
}
