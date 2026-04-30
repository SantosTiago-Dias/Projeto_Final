<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class FactContrato extends Model
{
    protected $connection = 'etl';
    protected $table = 'fact_contratos';
    public $timestamps = false;

    protected $primaryKey = null;
    public $incrementing = false;

    public function contrato(): BelongsTo
    {
        return $this->belongsTo(DimDetalhesContrato::class, 'chave_contratos');
    }

    public function entidade(): BelongsTo
    {
        return $this->belongsTo(DimEntidade::class, 'adjudicante');
    }

    public function entidade_concorrente(): BelongsTo
    {
        return $this->belongsTo(DimEntidade::class, 'chave_entidade', 'chave_entidade');
    }

    public function concorrentes(): HasMany
    {
        return $this->hasMany(FactContrato::class, 'chave_contratos', 'chave_contratos')
            ->with('entidade_concorrente');
    }

    public function tipo_contrato(): BelongsTo
    {
        return $this->belongsTo(TipoContrato::class, 'chave_tipo_contrato');
    }

    public function tipo_procedimento(): BelongsTo
    {
        return $this->belongsTo(TipoProcedimento::class, 'chave_tipo_procedimento');
    }

    public function data(): BelongsTo
    {
        return $this->belongsTo(DimData::class, 'chave_data');
    }
}
