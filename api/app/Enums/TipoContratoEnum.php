<?php

namespace App\Enums;

enum TipoContratoEnum: string
{
    case AquisicaoBensMoveis      = 'Aquisição de bens móveis';
    case AquisicaoServicos        = 'Aquisição de serviços';
    case ConcessaoObraPublicas    = 'Concessão de obras públicas';
    case ConcessaoServicosPublicos = 'Concessão de serviços públicas';
    case EmpreitadasObrasPublicas = 'Empreitadas de obras públicas';
    case LocacaoBensMoveis        = 'Locação de bens moveis';
    case Sociedade                = 'Sociedade';
    case Outros                   = 'Outros';

    public function label(): string
    {
        return match($this) {
            self::AquisicaoBensMoveis       => 'Aquisição de bens móveis',
            self::AquisicaoServicos         => 'Aquisição de serviços',
            self::ConcessaoObraPublicas     => 'Concessão de obras públicas',
            self::ConcessaoServicosPublicos => 'Concessão de serviços públicos',
            self::EmpreitadasObrasPublicas  => 'Empreitadas de obras públicas',
            self::LocacaoBensMoveis         => 'Locação de bens móveis',
            self::Sociedade                 => 'Sociedade',
            self::Outros                    => 'Outros',
        };
    }

    public static function toArray(): array
    {
        return array_map(
            fn($case) => ['value' => $case->value, 'label' => $case->label()],
            self::cases()
        );
    }
}
