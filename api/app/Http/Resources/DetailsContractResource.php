<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class DetailsContractResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'chave_contratos'                => $this->chave_contratos,
            'objeto'                         => $this->objeto,
            'descricao'                      => $this->descricao,
            'data_publicacao'                => $this->data_publicacao,
            'data_celebracao'                => $this->data_celebracao,
            'valor_contratual'               => $this->valor_contratual,
            'prazo_execucao'                 => $this->prazo_execucao,
            'local_execucao'                 => $this->local_execucao,
            'procedimento_centralizado'      => $this->procedimento_centralizado,
            'num_acordos_quadro'             => $this->num_acordos_quadro,
            'desc_acordo_quadro'             => $this->desc_acordo_quadro,
            'data_fecho_contrato'            => $this->data_fecho_contrato,
            'valor_total_efetivo'            => $this->valor_total_efetivo,
            'regime'                         => $this->regime,
            'tipo_fim_contrato'              => $this->tipo_fim_contrato,
            'crit_materiais'                 => $this->crit_materiais,
            'link_pecas'                     => $this->link_pecas,
            'observacoes'                    => $this->observacoes,
            'contrato_ecologico'             => $this->contrato_ecologico,
            'fundamentacao_ajuste_directo'   => $this->fundamentacao_ajuste_directo,
            'procedimento_centralizado' => $this->procedimento_centralizado,
            'cpvs'                           => CPVResource::collection($this->cpvs),
            'adjudicante'        => $this->whenLoaded('fact_contrato', fn() => new EntidadeResource($this->fact_contrato->first()->entidade)),
            'tipo_contrato'      => $this->whenLoaded('fact_contrato', fn() => new TipoContratoResource($this->fact_contrato->first()->tipo_contrato)),
            'tipo_procedimento'  => $this->whenLoaded('fact_contrato', fn() => new TipoProcedimentoResource($this->fact_contrato->first()->tipo_procedimento)),
            'data'               => $this->whenLoaded('fact_contrato', fn() => new DateResource($this->fact_contrato->first()->data)),
            'concorrentes'       => $this->whenLoaded('fact_contrato', fn() => ConcorrentesResource::collection($this->fact_contrato->first()->concorrentes ?? collect()))
        ];
    }
}
