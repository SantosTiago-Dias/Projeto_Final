<?php
namespace App\Filters;

use Illuminate\Database\Eloquent\Builder;

class ContratoFilter
{
    public static function apply(Builder $query, array $filters): Builder
    {
        //Tipo contrato
        $query=$query->when($filters['tipo_contrato'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.tipo_contrato', 'tipo', 'like', "%$v%"));

        //Tipo_procedimento
        $query=$query->when($filters['tipo_procedimento'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.tipo_procedimento', 'tipo', 'like', "%$v%"));

        return $query;
    }
}
