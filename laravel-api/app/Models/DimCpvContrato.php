<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DimCpvContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_cpv_contratos';
    public $timestamps = false;

     public function cpv()
    {
        return $this->belongsTo(Cpv::class, 'chave_cpv', 'id_cpv');
    }
}