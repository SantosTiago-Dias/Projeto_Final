DROP Table If EXISTS contratos_ext;

DROP Table If EXISTS entidades_ext;

DROP Table If EXISTS contratos_transf;

DROP Table If EXISTS entidade_transf;

DROP TABLE IF EXISTS detalhes_contratos_transf;

CREATE TABLE IF NOT EXISTS entidades_ext (
                                             id_entidade INTEGER,
                                             nif VARCHAR(20),
    nome VARCHAR(255),
    pais VARCHAR(255)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contratos_ext (
                                             id_contrato INT UNIQUE,
                                             tipo_contrato VARCHAR(255),
    tipo_procedimento VARCHAR(255),
    objeto TEXT,
    descricao TEXT,
    adjudicante TEXT,
    data_publicacao VARCHAR(10),
    data_celebracao VARCHAR(10),
    valor_contratual VARCHAR(20),
    cpvs VARCHAR(255),
    cpvsDesignation VARCHAR(255),
    prazo_execucao VARCHAR(255),
    local_execucao TEXT,
    fundamentacao VARCHAR(255),
    procedimento_centralizado VARCHAR(10),
    num_acordos_quadro VARCHAR(255),
    desc_acordo_quadro TEXT,
    data_fecho_contrato VARCHAR(10),
    valor_total_efetivo VARCHAR(20),
    regime VARCHAR(255),
    justificacao_nao_escrita TEXT,
    tipo_fim_contrato VARCHAR(255),
    crit_materiais VARCHAR(10),
    concorrentes TEXT,
    adjudicatarios TEXT,
    link_pecas VARCHAR(255),
    observacoes TEXT,
    contrato_ecologico VARCHAR(10),
    fundamentacao_ajuste_directo VARCHAR(255)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS entidade_transf (
                                               id_entidade INT,
                                               nif VARCHAR(20),
    nome VARCHAR(255),
    total_adjudicatario DECIMAL(15, 2),
    num_contratos_adjudicatario INT,
    total_adjudicante DECIMAL(15, 2),
    num_contratos_adjudicante INT,
    pais VARCHAR(255),
    distrito VARCHAR(255),
    UNIQUE (id_entidade)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS detalhes_contratos_transf (
                                                         id_contrato INT,
                                                         objeto TEXT,
                                                         descricao TEXT,
                                                         data_publicacao DATE,
                                                         data_celebracao DATE,
                                                         valor_contratual DECIMAL(15, 2),
    prazo_execucao INT,
    local_execucao TEXT,
    procedimento_centralizado VARCHAR(5),
    num_acordos_quadro VARCHAR(20),
    desc_acordo_quadro TEXT,
    data_fecho_contrato DATE,
    valor_total_efetivo DECIMAL(15, 2),
    regime VARCHAR(255),
    tipo_fim_contrato VARCHAR(255),
    crit_materiais VARCHAR(5),
    link_pecas VARCHAR(255),
    observacoes VARCHAR(255),
    contrato_ecologico VARCHAR(5),
    fundamentacao_ajuste_directo VARCHAR(255),
    UNIQUE (id_contrato)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contratos_transf (
                                                id_contrato INT,
                                                id_adjudicante INT,
                                                id_entidade INT,
                                                adjudicatario TINYINT(1),
    tipo_contrato VARCHAR(255),
    tipo_procedimento VARCHAR(255),
    fundamentacao VARCHAR(255),
    justificacao_nao_escrita TEXT,
    UNIQUE (id_contrato, id_entidade)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;