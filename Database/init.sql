/*
    FICHEIRO RESPONSVEL POR CRIAR A BASE DE DADOS 
*/

/*PARA DEFENIR AS BUFFERS*/
set global net_buffer_length=1000000; 
set global max_allowed_packet=1000000000;

/* CRIAR TABELAS DE EXTRAÇÃO */
CREATE TABLE IF NOT EXISTS cpv_dictionary_ext(
    id_cpv INT PRIMARY KEY auto_increment,
    codigo INT,
    descricao TEXT

);

CREATE TABLE IF NOT EXISTS tipo_procedimento_dictionary_ext (
    id_tipo_procedimento INT PRIMARY KEY auto_increment,
    tipo VARCHAR(255),
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS tipo_contrato_dictionary_ext (
    id_tipo_contrato INT PRIMARY KEY auto_increment,
    tipo VARCHAR(255),
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS justificacao_contrato_nao_escrito_dictionary_ext (
    id_justificacao INT PRIMARY KEY auto_increment,
    justificacao VARCHAR(255),
    descricao TEXT
);


CREATE TABLE IF NOT EXISTS fundamentacao_contrato_dictionary_ext (
    id_fundamentacao INT,
    fundamentacao VARCHAR(255),
    descricao TEXT
);


CREATE TABLE IF NOT EXISTS entidades_ext (
    id_entidade INTEGER,
    nif VARCHAR(20),
    nome VARCHAR(255),
    pais VARCHAR(50)
);


/*date so po load*/
CREATE TABLE IF NOT EXISTS contratos_ext (
    id_contrato INT UNIQUE,
    tipo_contrato VARCHAR(255),
    tipo_procedimento VARCHAR(255),
    objeto TEXT,--VARCHAR(255),
    descricao TEXT,--VARCHAR(255),
    /*adjudicatarios,*/
    adjudicante TEXT,
    data_publicacao VARCHAR(10),
    data_celebracao VARCHAR(10),
    valor_contratual VARCHAR(20),--DECIMAL(15,2),
    cpvs VARCHAR(12),
    cpvsDesignation VARCHAR(255),
    prazo_execucao VARCHAR(255),
    local_execucao VARCHAR(255),
    fundamentacao VARCHAR(255),
    procedimento_centralizado VARCHAR(10),--BOOLEAN,
    num_acordos_quadro VARCHAR(255),
    desc_acordo_quadro VARCHAR(255),
    data_fecho_contrato VARCHAR(10),
    valor_total_efetivo DECIMAL(15,2),
    regime VARCHAR(255),
    justificacao_nao_escrita VARCHAR(255),
    tipo_fim_contrato VARCHAR(255),
    crit_materiais VARCHAR(10),--BOOLEAN,
    concorrentes TEXT,
    adjudicatarios TEXT,
    link_pecas VARCHAR(255),
    observacoes VARCHAR(255),
    contrato_ecologico VARCHAR(10),--BOOLEAN,
    fundamentacao_ajuste_directo VARCHAR(255)
);
/* FIM DE CRIAÇÃO DAS TABELAS DE EXTRAÇÃO */

