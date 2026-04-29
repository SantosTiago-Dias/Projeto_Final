<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DimDetalhesContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'dim_detalhes_contratos';
    protected $primaryKey = 'chave_contratos';
    public $timestamps = false;

    public function cpvs()
    {
        return $this->hasMany(DimCpvContrato::class, 'chave_contrato', 'chave_contratos');
    }
}

