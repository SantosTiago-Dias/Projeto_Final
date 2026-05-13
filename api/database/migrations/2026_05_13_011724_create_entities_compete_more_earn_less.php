<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        DB::statement($this->createView());
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        DB::statement($this->dropView());
    }

    private function createView(): string
    {
        return <<<SQL
            CREATE VIEW  view_entidades_mais_concorrem_menos_ganham AS
            SELECT de.nome,
                COUNT(*) AS total_concursos,
                SUM(
                    CASE
                        WHEN ct.adjudicatario = 1 THEN 1
                        ELSE 0
                    END
                ) AS total_vitorias,
                SUM(
                    CASE
                        WHEN ct.adjudicatario = 0 THEN 1
                        ELSE 0
                    END
                ) AS total_derrotas,
                ROUND(
                    SUM(CASE WHEN ct.adjudicatario = 1 THEN 1 ELSE 0 END)
                    / COUNT(*) * 100,
                    2
                ) AS taxa_vitoria
            FROM fact_contratos ct
            LEFT JOIN dim_entidade de
                ON de.chave_entidade = ct.chave_entidade
            GROUP BY de.chave_entidade, de.nome
            HAVING COUNT(*) >= 5
            ORDER BY taxa_vitoria ASC, total_concursos DESC
            LIMIT 5;
        SQL;
    }

    private function dropView(): string
    {
        return <<<SQL
            DROP VIEW IF EXISTS view_entidades_mais_concorrem_menos_ganham
        SQL;
    }
};
