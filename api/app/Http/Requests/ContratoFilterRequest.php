<?php

namespace App\Http\Requests;

use App\Enums\TipoContratoEnum;
use App\Enums\TipoProcedimentoEnum;
use App\Models\TipoContrato;
use App\Models\TipoProcedimento;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Enum;

class ContratoFilterRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'tipo_contrato'     => ['nullable', Rule::exists(TipoContrato::class, 'id_tipo_contrato')->where(fn($q) => $q->where('id_tipo_contrato', '!=', 1))],
            'tipo_procedimento' => ['nullable', Rule::exists(TipoProcedimento::class, 'id_tipo_procedimento')->where(fn($q) => $q->where('id_tipo_procedimento', '!=', 1))],
            'data_publicacao_inicio'    => ['nullable', 'date_format:Y-m-d', 'before_or_equal:data_publicacao_fim'],
            'data_publicacao_fim'       => ['nullable', 'date_format:Y-m-d', 'after_or_equal:data_publicacao_inicio'],
            'valor_contratual_menor_que'          => ['nullable', 'numeric','min:0'],
            'valor_contratual_maior_que'          => ['nullable', 'numeric','min:0'],
            'prazo_execucao'            => ['nullable', 'integer','min:0'],
            'local_execucao'            => ['nullable', 'string','max:100', 'regex:/^[\pL\s\-]+$/u'],
            'cpvs'                      => ['nullable', 'string', 'max:100', 'regex:/^[\pL\d\s\-]+$/u'],
            'contrato_ecologico'        => ['nullable', 'in:0,1'],
            'procedimento_centralizado' => ['nullable', 'in:0,1'],
            'objeto' => ['nullable', 'string', 'max:255'],
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
