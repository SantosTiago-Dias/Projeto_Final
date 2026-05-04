<?php

namespace App\Http\Requests;

use App\Enums\TipoContratoEnum;
use App\Enums\TipoProcedimentoEnum;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Enum;

class ContratoFilterRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'tipo_contrato'             => ['nullable', new Enum(TipoContratoEnum::class)],
            'tipo_procedimento'         => ['nullable', new Enum(TipoProcedimentoEnum::class)],
            'data_publicacao_inicio'    => ['nullable', 'date_format:Y-m-d', 'before_or_equal:data_publicacao_fim'],
            'data_publicacao_fim'       => ['nullable', 'date_format:Y-m-d', 'after_or_equal:data_publicacao_inicio'],
            'valor_contratual'          => ['nullable', 'numeric','min:0'],
            'prazo_execucao'            => ['nullable', 'integer','min:0'],
            'cpvs'                      => ['nullable', 'string', 'max:100', 'regex:/^[\pL\s\-]+$/u'],
            'contrato_ecologico'        => ['nullable', 'in:0,1'],
            'procedimento_centralizado' => ['nullable', 'in:0,1'],
        ];
    }

    public function messages(): array
    {
        return [
            'tipo_contrato.enum' => 'Tipo de contrato invalido.',
            'tipo_procedimento.enum' => 'Tipo de procedimento invalido.',
            'data_publicacao_inicio.date_format' => 'A data de início deve estar no formato dd/mm/aaaa.',
            'data_publicacao_inicio.before_or_equal' => 'A data de início deve ser anterior ou igual à data de fim.',
            'data_publicacao_fim.date_format'  => 'A data de fim deve estar no formato dd/mm/aaaa.',
            'data_publicacao_fim.after_or_equal' => 'A data de fim deve ser posterior ou igual à data de início.',
            'valor_contratual.numeric'         => 'O valor contratual deve ser um número válido.',
            'valor_contratual.min'             => 'O valor contratual não pode ser negativo.',
            'prazo_execucao.integer' => 'O prazo de execução deve ser um número inteiro válido.',
            'prazo_execucao.min'     => 'O prazo de execução não pode ser negativo.',
            'cpvs.regex' => 'CPV invalido',
            'contrato_ecologico.in' => 'Contrato sustentavel invalido',
            'procedimento_centralizado.in' => 'Procedimento invalido',

        ];
    }
}
