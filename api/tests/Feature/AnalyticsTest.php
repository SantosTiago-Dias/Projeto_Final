<?php

namespace Tests\Feature;

use Tests\TestCase;

class AnalyticsTest extends TestCase
{
    public function test_can_get_biggest_contracts()
    {
        $response = $this->getJson('/api/analytics/biggest-contracts');

        $response->assertStatus(200);

        $response->assertJsonStructure([
                '*' => [
                    'chave_contratos',
                    'objeto',
                    'valor_contratual'
                ]
        ]);
    }

    public function test_can_get_smallest_contracts()
    {
        $response = $this->getJson('/api/analytics/smallest-contracts');

        $response->assertStatus(200);

        $response->assertJsonStructure([

                '*' => [
                    'chave_contratos',
                    'objeto',
                    'valor_contratual'
                ]

        ]);
    }

    public function test_can_get_entities_compete_more_earn_less()
    {
        $response = $this->getJson('/api/analytics/entitiesCompeteMoreEarnLess');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            '*' =>[
                'nome',
                'chave_entidade',
                'total_concursos',
                'total_vitorias',
                'total_derrotas',
                'taxa_vitoria',
            ]
        ]);
    }

    public function test_can_get_entities_more_contracts_as_contracting()
    {
        $response = $this->getJson('/api/analytics/entitiesMoreContractsAsContracting');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            [
                'nome',
                'numero_contratos',
                'adjudicante',
                'valor_adjudicado'
            ]
        ]);
    }

    public function test_can_search_cpv()
    {
        $response = $this->getJson('/api/analytics/search-cpv?query=test');

        $response->assertStatus(200);

        $response->assertJsonStructure([
                    'quantidade_contratos',
                    'valor_total'
        ]);
    }

    public function test_can_get_type_contracts()
    {
        $response = $this->getJson('/api/analytics/tipoContrato');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            '*' => [
                'chave_tipo_contrato',
                'contratos',
                'tipo_contrato' => [
                    'chave_tipo_contrato',
                    'tipo',
                    'descricao',
                ],
            ],
        ]);
    }

    public function test_can_get_type_procedures()
    {
        $response = $this->getJson('/api/analytics/tipoProcedimento');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            '*' => [
                'chave_tipo_procedimento',
                'contratos',
                'tipo_procedimento'=> [
                    'chave_tipo_procedimento',
                    'tipo',
                    'descricao',
                ],
            ]
        ]);
    }

    public function test_can_get_terms()
    {
        $response = $this->getJson('/api/terms');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            '*' => [
                'id',
                'term',
                'meaning'
            ]
        ]);
    }

}
