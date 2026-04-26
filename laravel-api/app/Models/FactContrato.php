<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class FactContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'fact_contratos';
    public $timestamps = false;

    protected $primaryKey = null;
    public $incrementing = false;

    public function contrato()
    {
        return $this->belongsTo(DimDetalhesContrato::class, 'chave_contratos');
    }

    public function entidade()
    {
        return $this->belongsTo(DimEntidade::class, 'chave_entidade');
    }

    public function adjudicante()
    {
        return $this->belongsTo(DimEntidade::class, 'adjudicante');
    }

    public function tipoContrato()
    {
        return $this->belongsTo(TipoContrato::class, 'chave_tipo_contrato');
    }

    public function tipoProcedimento()
    {
        return $this->belongsTo(TipoProcedimento::class, 'chave_tipo_procedimento');
    }

    public function data()
    {
        return $this->belongsTo(DimData::class, 'chave_data');
    }
}
