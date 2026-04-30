<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ListaContratosEntidadeResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'chave_contrato'=>$this->chave_contratos,
            'contrato' => new ContractsResource($this->contrato),
            'adjudicante' => new EntidadeResource($this->entidade),
            'concorrentes' => ConcorrentesResource::collection($this->concorrentes),
        ];
    }
}
