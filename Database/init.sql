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
    id_fundamentacao INT PRIMARY KEY auto_increment,
    fundamentacao VARCHAR(255),
    descricao TEXT
);


CREATE TABLE IF NOT EXISTS entidade_ext (
    id_entidade INT PRIMARY KEY auto_increment,
    nif VARCHAR(20),
    nome VARCHAR(255),
    /*num_contratos INT,-- dim fact load trigger to update */
    total_adjudicatario DECIMAL(15,2),
    num_contratos_adjudicatario  INT,
    total_adjudicante DECIMAL(15,2),
    num_contratos_adjudicante INT,
    pais VARCHAR(50)
);


/*date so po load*/
CREATE TABLE IF NOT EXISTS contratos_ext (
    id_contrato INT,
    tipo_contrato VARCHAR(255),
    tipo_procedimento VARCHAR(255),
    objeto VARCHAR(255),
    descricao VARCHAR(255),
    /*adjudicatarios,*/
    adjudicante_id INT,
    data_publicacao DATE,
    data_celebracao DATE,
    valor_contratual DECIMAL(15,2),
    cpv INT,
    cpv_description VARCHAR(255),
    prazo_execucao INT,
    local_execucao VARCHAR(255),
    fundamentacao VARCHAR(255),
    procedimento_centralizado BOOLEAN,
    num_acordos_quadro INT,
    desc_acordo_quadro VARCHAR(255),
    data_fecho_contrato DATE,
    valor_total_efetivo DECIMAL(15,2),
    regime VARCHAR(255),
    justificacao_nao_escrita VARCHAR(255),
    tipo_fim_contrato VARCHAR(255),
    crit_materiais BOOLEAN,
    /*concorrentes,*/
    link_pecas VARCHAR(255),
    observacoes VARCHAR(255),
    contrato_ecologico BOOLEAN,
    fundamentacao_ajuste_directo VARCHAR(255)
);
/* FIM DE CRIAÇÃO DAS TABELAS DE EXTRAÇÃO */