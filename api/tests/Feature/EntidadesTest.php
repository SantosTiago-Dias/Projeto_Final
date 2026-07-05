<?php

namespace Tests\Feature;

use Tests\TestCase;

class EntidadesTest extends TestCase
{
    public function test_can_get_entities_list()
    {
        $response = $this->getJson('/api/entidades');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            'data' => [
                '*' => [
                    'chave_entidade',
                    'nif',
                    'nome',
                    'num_contratos_adjudicatario',
                    'num_contratos_adjudicante',
                    'pais'
                ]
            ]
        ]);
    }

    public function test_can_get_single_entity()
    {
        $response = $this->getJson('/api/entidades/2');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            'chave_entidade',
            'id_entidade',
            'nif',
            'nome',
            'total_adjudicatario',
            'num_contratos_adjudicatario',
            'total_adjudicante',
            'num_contratos_adjudicante',
            'pais',
            'distrito'
        ]);
    }

    public function test_can_get_entity_contracts()
    {
        $response = $this->getJson('/api/entidades/2/listContratcs');

        $response->assertStatus(200);

        $response->assertJsonStructure([
            'data' => [
                '*' => [
                    'chave_contratos',
                    'id_contrato',
                    'objeto',
                    'descricao',
                    'valor_contratual',
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
}
