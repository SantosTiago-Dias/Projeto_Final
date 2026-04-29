<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TipoContratoResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id_tipo_contrato' => $this->id_tipo_contrato,
            'tipo' => $this->tipo,
            'descricao' => $this->descricao,
        ];
    }
}
