<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class EntidadeFilterRequest extends FormRequest
{
    public function rules(): array
    {
        return [

            'nome' => ['nullable', 'string', 'max:255'],
            'nif' => ['nullable','string','max:100'],
            'tipo_entidade' => ['nullable', 'in:1,2,3,5,6,7,8,9'],
            'pais' => ['nullable','string','max:100','regex:/^[\pL\s,\-]+$/u'],
            'num_contratos_adjudicatario_min' => ['nullable','integer','min:0'],
            'num_contratos_adjudicatario_max' => ['nullable','integer','min:0'],
            'num_contratos_adjudicante_min' => ['nullable','integer','min:0'],
            'num_contratos_adjudicante_max' => ['nullable','integer','min:0'],
        ];
    }

    public function messages(): array
    {
        return [

            'nome.string' => 'O nome da entidade é inválido.',
            'nome.max' => 'O nome da entidade excede o limite permitido.',
            'tipo_entidade.in' => 'Tipo de entidade inválido.',
            'pais.regex' => 'O país contém caracteres inválidos.',
            'num_contratos_adjudicatario_min.integer' => 'O número de contratos adjudicatário deve ser inteiro.',
            'num_contratos_adjudicatario_min.min' => 'O número de contratos adjudicatário não pode ser negativo.',
            'num_contratos_adjudicatario_max.integer' => 'O número de contratos adjudicatário deve ser inteiro.',
            'num_contratos_adjudicatario_max.min' => 'O número de contratos adjudicatário não pode ser negativo.',
            'num_contratos_adjudicante_min.integer' => 'O número de contratos adjudicante deve ser inteiro.',
            'num_contratos_adjudicante_min.min' => 'O número de contratos adjudicante não pode ser negativo.',
            'num_contratos_adjudicante_max.integer' => 'O número de contratos adjudicante deve ser inteiro.',
            'num_contratos_adjudicante_max.min' => 'O número de contratos adjudicante não pode ser negativo.',
        ];
    }
}
