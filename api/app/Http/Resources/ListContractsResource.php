<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use function Sodium\add;

class ListContractsResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {

        return [
            'chave_contratos'    => $this->chave_contratos,
            'id_contrato'        => $this->id_contrato,
            'objeto'             => $this->objeto,
            'descricao'          => $this->descricao,
            'data_publicacao'    => $this->data_publicacao,
            'valor_contratual'   => $this->valor_contratual,
            'contrato_ecologico' => $this->contrato_ecologico,
            'prazo_execucao' => $this->prazo_execucao,
            'procedimento_centralizado' => $this->procedimento_centralizado,

            'cpvs'               => CPVResource::collection($this->cpvs),
            'adjudicante'        => $this->whenLoaded('fact_contrato', fn() => new EntidadeResource($this->fact_contrato->first()->entidade)),
            'tipo_contrato'      => $this->whenLoaded('fact_contrato', fn() => new TipoContratoResource($this->fact_contrato->first()->tipo_contrato)),
            'tipo_procedimento'  => $this->whenLoaded('fact_contrato', fn() => new TipoProcedimentoResource($this->fact_contrato->first()->tipo_procedimento)),
            'data'               => $this->whenLoaded('fact_contrato', fn() => new DateResource($this->fact_contrato->first()->data)),

            // Concorrentes from the first fact row
            'concorrentes'       => $this->whenLoaded('fact_contrato', fn() => ConcorrentesResource::collection($this->fact_contrato->first()->concorrentes ?? collect())),
        ];
    }
}
