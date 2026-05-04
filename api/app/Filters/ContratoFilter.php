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

        //Data
        $query=$query->when($filters['data_publicacao_inicio'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.data', 'data', '>=', $v));
        $query=$query->when($filters['data_publicacao_fim'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.data', 'data','<=', $v));

        //valor contratual
        $query=$query->when($filters['valor_contratual'] ?? null , fn($q, $v) =>$q->where('valor_contratual','<=', $v));

        //prazo de execucao
        $query=$query->when($filters['prazo_execucao'] ?? null , fn($q, $v) =>$q->where('prazo_execucao','<=', $v));

        //CPV
        if ($filters['cpvs'] ?? false)
        {
            $keyword = strip_tags($filters['cpvs']);
            $query = $query->when($keyword, fn($q, $v) => $q->whereHas('cpvs.cpv', fn($q2) => $q2->where('descricao', 'LIKE', '%' . $keyword . '%')));
        }


        //contrato ecologico
        $query=$query->when($filters['contrato_ecologico'] ?? null , fn($q, $v) =>$q->where('contrato_ecologico','=',$v));

        //procedimento centralizado
        $query=$query->when($filters['procedimento_centralizado'] ?? null , fn($q, $v) =>$q->where('procedimento_centralizado','=', $v));

        return $query;
    }
}
