CREATE TABLE IF NOT EXISTS entidade_transf (
    id_entidade INT,
    nif VARCHAR(20),
    nome VARCHAR(255),
    total_adjudicatario DECIMAL(15,2),
    num_contratos_adjudicatario INT,
    total_adjudicante DECIMAL(15,2),
    num_contratos_adjudicante INT,
    pais VARCHAR(50),
    UNIQUE (id_entidade)
);

CREATE TABLE IF NOT EXISTS detalhes_contratos_transf (
    id_contrato INT,
    objeto TEXT,
    descricao TEXT,
    data_publicacao DATE,
    data_celebracao DATE,
    valor_contratual DECIMAL(15,2),
    prazo_execucao INT,
    local_execucao VARCHAR(255),
    procedimento_centralizado TINYINT(1),
    num_acordos_quadro VARCHAR(20),
    desc_acordo_quadro VARCHAR(255),
    data_fecho_contrato DATE,
    valor_total_efetivo DECIMAL(15,2),
    regime VARCHAR(255),
    tipo_fim_contrato VARCHAR(255),
    crit_materiais TINYINT(1),
    link_pecas VARCHAR(255),
    observacoes VARCHAR(255),
    contrato_ecologico TINYINT(1),
    fundamentacao_ajuste_directo VARCHAR(255),
    UNIQUE (id_contrato)
);

CREATE TABLE IF NOT EXISTS contratos_transf (
    id_contrato INT,
    id_adjudicante INT,
    id_entidade INT,
    adjudicatario TINYINT(1),
    chave_tipo_contrato INT,
    chave_tipo_procedimento INT,
    chave_fundamentacao INT,
    chave_justificacao_nao_escrita INT,
    UNIQUE (id_contrato, id_entidade)
);

CREATE TABLE IF NOT EXISTS cpv_contratos_transf (
    id_contrato INT,
    cpv VARCHAR(10),
    cpv_descricao VARCHAR(255),
    UNIQUE (id_contrato, cpv)
);