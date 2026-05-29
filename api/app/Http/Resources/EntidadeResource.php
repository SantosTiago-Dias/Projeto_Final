<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class EntidadeResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'chave_entidade' => $this->chave_entidade,
            'id_entidade' => $this->id_entidade,
            'nif' => $this->nif,
            'nome' => $this->nome,
            'num_contratos_adjudicatario' => $this->num_contratos_adjudicatario,
            'num_contratos_adjudicante' => $this->num_contratos_adjudicante,
            'pais'=>$this->pais,
        ];
    }
}
