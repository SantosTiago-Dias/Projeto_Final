<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ContractsResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
                'id'               => $this->id_contrato,
                'objeto'           => $this->objeto,
                'descricao'        => $this->descricao,
                'data_publicacao'  => $this->data_publicacao,
                'data_celebracao'  => $this->data_celebracao,
                'valor_contratual'   => $this->valor_contratual,
                'prazo_execucao' => $this->prazo_execucao,
                'local_execucao'   => $this->local_execucao,
                'procedimento_centralizado' => $this->procedimento_centralizado,
                'num_acordos_quadro' => $this->num_acordos_quadro,
                'desc_acordo_quadro' => $this->desc_acordo_quadro,
                'data_fecho_contrato' => $this->data_fecho_contrato,
                'valor_total_efetivo' => $this->valor_total_efetivo,
                'regime' => $this->regime,
                'tipo_fim_contrato' => $this->tipo_fim_contrato,
                'crit_materiais' => $this->crit_materiais,
                'link_pecas' => $this->link_pecas,
                'observacoes' => $this->observacoes,
                'contrato_ecologico' => $this->contrato_ecologico,
                'fundamentacao_ajuste_directo' => $this->fundamentacao_ajuste_directo,
                'cpvs'             => CPVResource::collection($this->cpvs)
        ];
    }
}
