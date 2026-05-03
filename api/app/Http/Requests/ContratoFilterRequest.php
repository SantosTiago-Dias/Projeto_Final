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
            'tipo_contrato'       => ['nullable', new Enum(TipoContratoEnum::class)],
            'tipo_procedimento' =>['nullable', new Enum(TipoProcedimentoEnum::class)],
        ];
    }

    public function messages(): array
    {
        return [
            'tipo_contrato.enum' => 'Tipo de contrato invalido.',
            'tipo_procedimento.enum' => 'Tipo de procedimento invalido.',
        ];
    }
}
