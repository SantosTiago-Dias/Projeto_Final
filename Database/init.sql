
/* DEFINIR BUFFERS */
SET GLOBAL net_buffer_length  = 1000000;
SET GLOBAL max_allowed_packet = 1000000000;

/*Limpeza de tabelas*/
DROP Table If EXISTS contratos_ext;
DROP Table If EXISTS entidades_ext;
DROP Table If EXISTS contratos_transf;
DROP Table If EXISTS entidade_transf;
DROP TABLE IF EXISTS detalhes_contratos_transf;

CREATE TABLE IF NOT EXISTS data_extracted(
    id INT PRIMARY KEY AUTO_INCREMENT,
    num_contratos INT,
    media_contratos DECIMAL(15,2),
    data_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_logs_extract (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto     VARCHAR(50) NOT NULL,
    status          ENUM('INICIO','SUCESSO','ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem        TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS t_logs_transformacao (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto     VARCHAR(255) NOT NULL,
    status          ENUM('INICIO','SUCESSO','ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem        TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_logs_carregamento (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto     VARCHAR(50) NOT NULL,
    status          ENUM('INICIO','SUCESSO','ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem        TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cpv_dictionary (
    id_cpv   INT PRIMARY KEY AUTO_INCREMENT,
    codigo   VARCHAR(10),
    cpv_descricao VARCHAR(255),
    descricao TEXT,
    UNIQUE (codigo)
);

CREATE TABLE IF NOT EXISTS tipo_procedimento_dictionary (
    id_tipo_procedimento INT PRIMARY KEY AUTO_INCREMENT,
    tipo                 VARCHAR(255),
    descricao            TEXT,
    UNIQUE (tipo)
);

CREATE TABLE IF NOT EXISTS tipo_contrato_dictionary (
    id_tipo_contrato INT PRIMARY KEY AUTO_INCREMENT,
    tipo             VARCHAR(255),
    descricao        TEXT,
    UNIQUE (tipo)
);

CREATE TABLE IF NOT EXISTS justificacao_contrato_nao_escrito_dictionary (
    id_justificacao INT PRIMARY KEY AUTO_INCREMENT,
    justificacao    TEXT,
    descricao       TEXT,
    UNIQUE (justificacao(500))
);

CREATE TABLE IF NOT EXISTS fundamentacao_contrato_dictionary (
    id_fundamentacao INT PRIMARY KEY AUTO_INCREMENT,
    fundamentacao    VARCHAR(255),
    descricao        TEXT,
    UNIQUE (fundamentacao)
);

CREATE TABLE IF NOT EXISTS entidades_ext (
    id_entidade INTEGER,
    nif         VARCHAR(20),
    nome        VARCHAR(255),
    pais        VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS contratos_ext (
    id_contrato               INT UNIQUE,
    tipo_contrato             VARCHAR(255),
    tipo_procedimento         VARCHAR(255),
    objeto                    TEXT,
    descricao                 TEXT,
    adjudicante               TEXT,
    data_publicacao           VARCHAR(10),
    data_celebracao           VARCHAR(10),
    valor_contratual          VARCHAR(20),
    cpvs                      VARCHAR(255),
    cpvsDesignation           VARCHAR(255),
    prazo_execucao            VARCHAR(255),
    local_execucao            TEXT,
    fundamentacao             VARCHAR(255),
    procedimento_centralizado VARCHAR(10),
    num_acordos_quadro        VARCHAR(255),
    desc_acordo_quadro        TEXT,
    data_fecho_contrato       VARCHAR(10),
    valor_total_efetivo       VARCHAR(20),
    regime                    VARCHAR(255),
    justificacao_nao_escrita  TEXT,
    tipo_fim_contrato         VARCHAR(255),
    crit_materiais            VARCHAR(10),
    concorrentes              TEXT,
    adjudicatarios            TEXT,
    link_pecas                VARCHAR(255),
    observacoes               TEXT,
    contrato_ecologico        VARCHAR(10),
    fundamentacao_ajuste_directo VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS entidade_transf (
    id_entidade                 INT,
    nif                         VARCHAR(20),
    nome                        VARCHAR(255),
    total_adjudicatario         DECIMAL(15,2),
    num_contratos_adjudicatario INT,
    total_adjudicante           DECIMAL(15,2),
    num_contratos_adjudicante   INT,
    pais                        VARCHAR(255),
    UNIQUE (id_entidade)
);

CREATE TABLE IF NOT EXISTS detalhes_contratos_transf (
    id_contrato               INT,
    objeto                    TEXT,
    descricao                 TEXT,
    data_publicacao           DATE,
    data_celebracao           DATE,
    valor_contratual          DECIMAL(15,2),
    prazo_execucao            INT,
    local_execucao            TEXT,
    procedimento_centralizado TINYINT(1),
    num_acordos_quadro        VARCHAR(20),
    desc_acordo_quadro        TEXT,
    data_fecho_contrato       DATE,
    valor_total_efetivo       DECIMAL(15,2),
    regime                    VARCHAR(255),
    tipo_fim_contrato         VARCHAR(255),
    crit_materiais            TINYINT(1),
    link_pecas                VARCHAR(255),
    observacoes               VARCHAR(255),
    contrato_ecologico        TINYINT(1),
    fundamentacao_ajuste_directo VARCHAR(255),
    UNIQUE (id_contrato)
);

CREATE TABLE IF NOT EXISTS contratos_transf (
    id_contrato                  INT,
    id_adjudicante               INT,
    id_entidade                  INT,
    adjudicatario                TINYINT(1),
    tipo_contrato          VARCHAR(255),
    tipo_procedimento      VARCHAR(255),
    fundamentacao          VARCHAR(255),
    justificacao_nao_escrita TEXT,
    UNIQUE (id_contrato, id_entidade)
);

CREATE TABLE IF NOT EXISTS cpv_contratos_transf (
    id_contrato   INT,
    cpv           VARCHAR(10),
    cpv_descricao VARCHAR(255),
    UNIQUE (id_contrato, cpv)
);
CREATE TABLE IF NOT EXISTS dim_entidade (
    chave_entidade              INT AUTO_INCREMENT PRIMARY KEY,
    id_entidade                 INT,
    nif                         VARCHAR(20),
    nome                        VARCHAR(255),
    total_adjudicatario         DECIMAL(15,2),
    num_contratos_adjudicatario INT,
    total_adjudicante           DECIMAL(15,2),
    num_contratos_adjudicante   INT,
    pais                        VARCHAR(255),
    UNIQUE (id_entidade)
);

CREATE TABLE IF NOT EXISTS dim_detalhes_contratos (
    chave_contratos           INT AUTO_INCREMENT PRIMARY KEY,
    id_contrato               INT,
    objeto                    TEXT,
    descricao                 TEXT,
    data_publicacao           DATE,
    data_celebracao           DATE,
    valor_contratual          DECIMAL(15,2),
    prazo_execucao            INT,
    local_execucao            TEXT,
    procedimento_centralizado TINYINT(1),
    num_acordos_quadro        VARCHAR(20),
    desc_acordo_quadro        TEXT,
    data_fecho_contrato       DATE,
    valor_total_efetivo       DECIMAL(15,2),
    regime                    VARCHAR(255),
    tipo_fim_contrato         VARCHAR(255),
    crit_materiais            TINYINT(1),
    link_pecas                VARCHAR(255),
    observacoes               VARCHAR(255),
    contrato_ecologico        TINYINT(1),
    fundamentacao_ajuste_directo VARCHAR(255),
    UNIQUE (id_contrato)
);

CREATE TABLE IF NOT EXISTS dim_cpv_contratos (
    chave_contrato INT,
    chave_cpv      INT,
    UNIQUE  (chave_contrato, chave_cpv),
    PRIMARY KEY (chave_contrato, chave_cpv),
    FOREIGN KEY (chave_contrato) REFERENCES dim_detalhes_contratos(chave_contratos)
);

CREATE TABLE IF NOT EXISTS dim_data (
    chave_date INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    feriado VARCHAR(100),
    fim_semana TINYINT(1),
    dia TINYINT,
    mes TINYINT,
    ano SMALLINT,
    dia_semana VARCHAR(20),
    nome_mes VARCHAR(20),
    abr_mes VARCHAR(5),
    data_extenso VARCHAR(100),
    evento_natural VARCHAR(255),
    UNIQUE (data)
);

CREATE TABLE IF NOT EXISTS fact_contratos (
    chave_contratos               INT,
    adjudicante                   INT,
    chave_entidade                INT,
    adjudicatario                 TINYINT(1),
    chave_tipo_contrato           INT,
    chave_tipo_procedimento       INT,
    chave_fundamentacao           INT,
    chave_justificacao_nao_escrita INT,
    valor_contratual              DECIMAL(15,2),
    chave_data                     INT,
    PRIMARY KEY (chave_contratos, chave_entidade, adjudicante),
    FOREIGN KEY (chave_contratos) REFERENCES dim_detalhes_contratos(chave_contratos),
    FOREIGN KEY (chave_entidade)  REFERENCES dim_entidade(chave_entidade),
    FOREIGN KEY (chave_tipo_contrato) REFERENCES tipo_contrato_dictionary(id_tipo_contrato),
    FOREIGN KEY (chave_tipo_procedimento) REFERENCES tipo_procedimento_dictionary(id_tipo_procedimento),
    FOREIGN KEY (chave_fundamentacao) REFERENCES fundamentacao_contrato_dictionary(id_fundamentacao),
    FOREIGN KEY (chave_justificacao_nao_escrita) REFERENCES justificacao_contrato_nao_escrito_dictionary(id_justificacao),
    FOREIGN KEY (chave_data) REFERENCES dim_data(chave_date)
);


-- =====================
-- INSERTS DOS VALORES NULOS
-- =====================

INSERT INTO dim_entidade ( id_entidade, nif, nome, total_adjudicatario, num_contratos_adjudicatario, total_adjudicante, num_contratos_adjudicante, pais)
VALUES (-1, NULL, 'ENTIDADE INVALIDA', 0, 0, 0, 0, 'N/A');

INSERT INTO dim_detalhes_contratos (id_contrato, objeto, descricao,data_publicacao, data_celebracao,valor_contratual, prazo_execucao,
    local_execucao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo,
    regime, tipo_fim_contrato, crit_materiais, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo
) VALUES (-1, 'N/A', 'CONTRATO INVALIDO', NULL, NULL, 0, 0, 'N/A', 0, 'N/A', 'N/A',NULL, 0, 'N/A', 'N/A', 0, 'N/A', 'N/A', 0, 'N/A');

INSERT INTO dim_data (data, feriado, fim_semana, dia, mes, ano, dia_semana, nome_mes,abr_mes, evento_natural, data_extenso)
VALUES ( NULL, 'N/A', NULL, NULL, NULL, NULL,'N/A', 'N/A', 'N/A', 'N/A', 'DATA INVALIDA');

INSERT INTO cpv_dictionary (codigo, cpv_descricao, descricao) VALUES ('N/A', 'N/A', 'VALOR DESCONHECIDO');

INSERT INTO tipo_procedimento_dictionary (tipo, descricao) VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT INTO tipo_contrato_dictionary (tipo, descricao) VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT INTO justificacao_contrato_nao_escrito_dictionary (justificacao, descricao) VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT INTO fundamentacao_contrato_dictionary (fundamentacao, descricao) VALUES ('N/A', 'VALOR DESCONHECIDO');
