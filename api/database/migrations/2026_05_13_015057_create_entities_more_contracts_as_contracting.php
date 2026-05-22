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
            CREATE VIEW  view_entidades_mais_contratos_adjudicados AS
            SELECT nome, count(*) AS numero_contratos
            FROM fact_contratos ct
            LEFT JOIN dim_entidade deadjudicante
                            ON deadjudicante.chave_entidade = ct.adjudicante
            GROUP BY adjudicante
            ORDER BY count(*) desc
            LIMIT 5;
        SQL;
    }

    private function dropView(): string
    {
        return <<<SQL
            DROP VIEW IF EXISTS view_entidades_mais_contratos_adjudicados
        SQL;
    }
};
