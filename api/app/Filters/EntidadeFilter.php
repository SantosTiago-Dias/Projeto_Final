<?php

namespace App\Filters;

use Illuminate\Database\Eloquent\Builder;

class EntidadeFilter
{
    public static function apply(Builder $query, array $filters): Builder
    {

        // Nome
        $query = $query->when(
            $filters['nome'] ?? null,fn($q, $v) => $q->where('nome', 'LIKE', '%' . strtoupper(trim($v)) . '%'));

        // NIF
        $query = $query->when($filters['nif'] ?? null,fn($q, $v) =>$q->where('nif', '=', $v));

        $query = $query->when(
            $filters['tipo_entidade'] ?? null,fn($q, $v) => $q->where('nif', 'like', $v . '%'));

        // País
        $query = $query->when(
            $filters['pais'] ?? null,fn($q, $v) =>$q->where('pais', 'LIKE', '%' . strtoupper(trim($v)) . '%') );

        // Distrito
        $query = $query->when(
            $filters['distrito'] ?? null,fn($q, $v) => $q->where('distrito', '=', strtoupper(trim($v))));

        // Número contratos adjudicatário mínimo
        $query = $query->when(
            $filters['num_contratos_adjudicatario_min'] ?? null,fn($q, $v) =>$q->where('num_contratos_adjudicatario', '>=', $v));

        // Número contratos adjudicatário máximo
        $query = $query->when(
            $filters['num_contratos_adjudicatario_max'] ?? null,fn($q, $v) =>$q->where('num_contratos_adjudicatario', '<=', $v));

        // Número contratos adjudicante mínimo
        $query = $query->when(
            $filters['num_contratos_adjudicante_min'] ?? null,fn($q, $v) =>$q->where('num_contratos_adjudicante', '>=', $v));

        // Número contratos adjudicante máximo
        $query = $query->when(
            $filters['num_contratos_adjudicante_max'] ?? null,fn($q, $v) =>$q->where('num_contratos_adjudicante', '<=', $v));

        return $query;
    }
}
