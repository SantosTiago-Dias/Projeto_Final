<?php

namespace App\Enums;

enum TipoProcedimentoEnum: string
{
    case ConsultaPrevia                                    = 'Consulta Prévia';
    case AjusteDirectoRegimeGeral                          = 'Ajuste Direto Regime Geral';
    case ConcursoPublico                                   = 'Concurso público';
    case ConcursoLimitadoPreviaQualificacao                = 'Concurso limitado por prévia qualificação';
    case ProcedimentoNegociacao                            = 'Procedimento de negociação';
    case DialogoConcorrencial                              = 'Diálogo concorrencial';
    case AcordoQuadroArt258                                = 'Ao abrigo de acordo-quadro (art.º 258.º)';
    case AcordoQuadroArt259                                = 'Ao abrigo de acordo-quadro (art.º 259.º)';
    case ParceriaInovacao                                  = 'Parceria para a inovação';
    case DisponibilizacaoBensMoveis                        = 'Disponibilização de bens móveis';
    case ServicosSociaisOutrosServicosEspecificos          = 'Serviços sociais e outros serviços específicos';
    case ConcursoConcecaoSimplificado                      = 'Concurso de conceção simplificado';
    case ConcursoIdeiasSimplificado                        = 'Concurso de ideias simplificado';
    case ConsultaPreviaSimplificada                        = 'Consulta Prévia Simplificada';
    case ConcursoPublicoSimplificado                       = 'Concurso público simplificado';
    case ConcursoLimitadoPreviaQualificacaoSimplificado    = 'Concurso limitado por prévia qualificação simplificado';
    case AjusteDirectoRegimeGeralArt7Lei30_2021            = 'Ajuste Direto Regime Geral ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05';
    case ConsultaPreviaArt7Lei30_2021                      = 'Consulta prévia ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05';
    case AjusteDirectoSimplificado                         = 'Ajuste direto simplificado';
    case AjusteDirectoSimplificadoLei30_2021               = 'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05';
    case SetoresEspeciaisIsencaoParteII                    = 'Setores especiais – isenção parte II';
    case ContratacaoExcluidaII                             = 'Contratação excluída II';

    public function label(): string
    {
        return match($this) {
            self::ConsultaPrevia                                    => 'Consulta Prévia',
            self::AjusteDirectoRegimeGeral                          => 'Ajuste Direto Regime Geral',
            self::ConcursoPublico                                   => 'Concurso público',
            self::ConcursoLimitadoPreviaQualificacao                => 'Concurso limitado por prévia qualificação',
            self::ProcedimentoNegociacao                            => 'Procedimento de negociação',
            self::DialogoConcorrencial                              => 'Diálogo concorrencial',
            self::AcordoQuadroArt258                                => 'Ao abrigo de acordo-quadro (art.º 258.º)',
            self::AcordoQuadroArt259                                => 'Ao abrigo de acordo-quadro (art.º 259.º)',
            self::ParceriaInovacao                                  => 'Parceria para a inovação',
            self::DisponibilizacaoBensMoveis                        => 'Disponibilização de bens móveis',
            self::ServicosSociaisOutrosServicosEspecificos          => 'Serviços sociais e outros serviços específicos',
            self::ConcursoConcecaoSimplificado                      => 'Concurso de conceção simplificado',
            self::ConcursoIdeiasSimplificado                        => 'Concurso de ideias simplificado',
            self::ConsultaPreviaSimplificada                        => 'Consulta Prévia Simplificada',
            self::ConcursoPublicoSimplificado                       => 'Concurso público simplificado',
            self::ConcursoLimitadoPreviaQualificacaoSimplificado    => 'Concurso limitado por prévia qualificação simplificado',
            self::AjusteDirectoRegimeGeralArt7Lei30_2021            => 'Ajuste Direto Regime Geral ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05',
            self::ConsultaPreviaArt7Lei30_2021                      => 'Consulta prévia ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05',
            self::AjusteDirectoSimplificado                         => 'Ajuste direto simplificado',
            self::AjusteDirectoSimplificadoLei30_2021               => 'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05',
            self::SetoresEspeciaisIsencaoParteII                    => 'Setores especiais – isenção parte II',
            self::ContratacaoExcluidaII                             => 'Contratação excluída II',
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
