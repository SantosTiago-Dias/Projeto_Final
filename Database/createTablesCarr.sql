CREATE TABLE IF NOT EXISTS dim_entidade (
    chave_entidade INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS dim_detalhes_contratos (
    chave_contratos INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS dim_cpv_contratos (
    chave_contrato INT,
    cpv VARCHAR(10),
    UNIQUE (chave_contrato, cpv),
    
    PRIMARY KEY (chave_contrato, cpv),
    FOREIGN KEY (chave_contrato) REFERENCES dim_detalhes_contratos(chave_contratos)
);

CREATE TABLE IF NOT EXISTS fact_contratos (
    chave_contratos INT,
    adjudicante INT,
    chave_entidade INT,
    adjudicatario TINYINT(1),
    chave_tipo_contrato INT,
    chave_tipo_procedimento INT,
    chave_fundamentacao INT,
    chave_justificacao_nao_escrita INT,

    valor_contratual DECIMAL(15,2),
    data_celebracao DATE,

    PRIMARY KEY (chave_contratos, chave_entidade),
    FOREIGN KEY (chave_contratos) REFERENCES dim_detalhes_contratos(chave_contratos),
    FOREIGN KEY (chave_entidade) REFERENCES dim_entidade(chave_entidade)
);



