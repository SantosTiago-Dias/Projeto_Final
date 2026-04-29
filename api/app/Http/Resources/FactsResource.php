<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class FactsResource extends JsonResource
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
            'entidade' => new EntidadeResource($this->entidade),
            'concorrentes' => ConcorrentesResource::collection($this->concorrentes),
            'tipo_contrato' => new TipoContratoResource($this->tipo_contrato),
            'tipo_procedimento' => new TipoProcedimentoResource($this->tipo_procedimento),
            'data' => new DateResource($this->data)
        ];
    }
}
