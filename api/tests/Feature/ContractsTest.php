<?php

namespace Tests\Feature;

use Tests\TestCase;

class ContractsTest extends TestCase
{
    public function test_can_get_contracts_list()
    {
        $response = $this->getJson('/api/contracts');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            'data' => [
                '*' => [
                    'chave_contratos',
                    'id_contrato',
                    'objeto',
                    'descricao',
                    'valor_contratual',
                    'contrato_ecologico',
                    'prazo_execucao',
                    'procedimento_centralizado',

                    'cpvs',
                    'adjudicante',
                    'tipo_contrato',
                    'tipo_procedimento',
                    'data',
                    'concorrentes'
                ]
            ]
        ]);
    }

    public function test_can_get_single_contract()
    {
        $response = $this->getJson('/api/contracts/2');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            'chave_contratos',
            'objeto',
            'descricao',
            'data_publicacao',
            'data_celebracao',
            'valor_contratual',
            'prazo_execucao',
            'local_execucao',
            'procedimento_centralizado',
            'num_acordos_quadro',
            'desc_acordo_quadro',
            'data_fecho_contrato',
            'valor_total_efetivo',
            'regime',
            'tipo_fim_contrato',
            'crit_materiais',
            'link_pecas',
            'observacoes',
            'contrato_ecologico',
            'fundamentacao_ajuste_directo',
            'cpvs',
            'adjudicante',
            'tipo_contrato',
            'tipo_procedimento',
            'data',
            'concorrentes'
        ]);
    }

    public function test_can_get_filters()
    {
        $response = $this->getJson('/api/contracts/getFilters');

        $response->assertStatus(200);
    }
}
