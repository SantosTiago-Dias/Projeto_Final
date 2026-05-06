<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class CPVResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id_cpv'=> $this->cpv->id_cpv,
            'codigo' => $this->cpv->codigo,
            'cpv_descricao' => $this->cpv->cpv_descricao,
            'descricao' => $this->cpv->descricao,

        ];
    }
}
