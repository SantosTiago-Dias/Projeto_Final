<?php
namespace App\Filters;

use Illuminate\Database\Eloquent\Builder;

class ContratoFilter
{
    public static function apply(Builder $query, array $filters): Builder
    {
        //Tipo contrato
        $query=$query->when($filters['tipo_contrato'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.tipo_contrato', 'chave_tipo_contrato', 'like', $v));

        //Tipo_procedimento
        $query=$query->when($filters['tipo_procedimento'] ?? null, fn($q, $v) =>$q->whereRelation('fact_contrato.tipo_procedimento', 'chave_tipo_procedimento', 'like', $v));

        //Data
        $query=$query->when($filters['data_publicacao_inicio'] ?? null, fn($q, $v) =>$q->where('data_publicacao', '>=', $v));
        $query=$query->when($filters['data_publicacao_fim'] ?? null, fn($q, $v) =>$q->where('data_publicacao', '<=', $v));

        //valor contratual
        $query=$query->when($filters['valor_contratual_menor_que'] ?? null , fn($q, $v) =>$q->where('valor_contratual','<=', $v));
        $query=$query->when($filters['valor_contratual_maior_que'] ?? null , fn($q, $v) =>$q->where('valor_contratual','>=', $v));

        //prazo de execucao
        $query=$query->when($filters['prazo_execucao'] ?? null , fn($q, $v) =>$q->where('prazo_execucao','<=', $v));

        //local de execucao
        $query=$query->when($filters['local_execucao'] ?? null , fn($q, $v) =>$q->where('local_execucao', 'LIKE', '%' . $v . '%'));

        //CPV
        if ($filters['cpvs'] ?? false)
        {

            $keyword = strip_tags($filters['cpvs']);
            $query = $query->when($keyword, fn($q, $v) => $q->whereHas('cpvs.cpv', fn($q2) => $q2->where('descricao', 'LIKE', '%' . $keyword . '%')->orWhere('cpv_descricao', 'LIKE', '%' . $keyword . '%')->orWhere('codigo', '=',$keyword)));
        }


        //contrato ecologico
        $query=$query->when($filters['contrato_ecologico'] ?? null , fn($q, $v) =>$q->where('contrato_ecologico','=',$v));

        //procedimento centralizado
        $query=$query->when($filters['procedimento_centralizado'] ?? null , fn($q, $v) =>$q->where('procedimento_centralizado','=', $v));

        // Objeto
        $query = $query->when(
            $filters['objeto'] ?? null,fn($q, $v) => $q->where('objeto', 'like', '%' . $v . '%'));

        return $query;
    }
}
