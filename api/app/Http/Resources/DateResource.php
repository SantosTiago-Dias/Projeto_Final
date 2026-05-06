<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class DateResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'date'=> $this->data,
            'feriado'=> $this->feriado,
            'fim_semana' => $this->fim_semana,
            'data_extenso' => $this->data_extenso,
            'evento_natural' => $this->evento_natural
        ];
    }
}
