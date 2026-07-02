/* DEFINIR BUFFERS */
SET GLOBAL net_buffer_length = 1000000;
SET GLOBAL max_allowed_packet = 1000000000;

-- Terms Table
CREATE TABLE IF NOT EXISTS terms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    term VARCHAR(255) NOT NULL,
    meaning VARCHAR(255) NOT NULL
    );

-- Cache Table
CREATE TABLE `cache` (
    `key`        VARCHAR(255)  NOT NULL,
    `value`      MEDIUMTEXT    NOT NULL,
    `expiration` BIGINT        NOT NULL,
    PRIMARY KEY (`key`),
    INDEX `cache_expiration_index` (`expiration`)
);
 
-- Cache Locks Table
CREATE TABLE `cache_locks` (
    `key`        VARCHAR(255)  NOT NULL,
    `owner`      VARCHAR(255)  NOT NULL,
    `expiration` BIGINT        NOT NULL,
    PRIMARY KEY (`key`),
    INDEX `cache_locks_expiration_index` (`expiration`)
);

CREATE TABLE IF NOT EXISTS data_extracted (
    id INT PRIMARY KEY AUTO_INCREMENT,
    num_contratos INT,
    media_contratos DECIMAL(15, 2),
    data_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_logs_extract (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto VARCHAR(50) NOT NULL,
    status ENUM('INICIO', 'SUCESSO', 'ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_logs_transformacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto VARCHAR(255) NOT NULL,
    status ENUM('INICIO', 'SUCESSO', 'ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS t_logs_carregamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_objeto VARCHAR(50) NOT NULL,
    status ENUM('INICIO', 'SUCESSO', 'ERRO') NOT NULL DEFAULT 'INICIO',
    mensagem TEXT,
    ultima_extracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cpv_dictionary (
    id_cpv INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10),
    cpv_descricao VARCHAR(255),
    descricao TEXT,
    UNIQUE (codigo)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tipo_procedimento_dictionary (
    id_tipo_procedimento INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(255),
    descricao TEXT,
    UNIQUE (tipo)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tipo_contrato_dictionary (
    id_tipo_contrato INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(255),
    descricao TEXT,
    UNIQUE (tipo)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS justificacao_contrato_nao_escrito_dictionary (
    id_justificacao INT PRIMARY KEY AUTO_INCREMENT,
    justificacao TEXT,
    descricao TEXT,
    UNIQUE (justificacao (500))
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fundamentacao_contrato_dictionary (
    id_fundamentacao INT PRIMARY KEY AUTO_INCREMENT,
    fundamentacao VARCHAR(255),
    descricao TEXT,
    UNIQUE (fundamentacao)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cpv_dim (
    chave_cpv INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10),
    cpv_descricao VARCHAR(255),
    descricao TEXT,
    UNIQUE (codigo),
    FULLTEXT (codigo, cpv_descricao, descricao)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tipo_procedimento_dim (
    chave_tipo_procedimento INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(255),
    descricao TEXT,
    UNIQUE (tipo)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tipo_contrato_dim (
    chave_tipo_contrato INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(255),
    descricao TEXT,
    UNIQUE (tipo)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS justificacao_contrato_nao_escrito_dim (
    chave_justificacao INT PRIMARY KEY AUTO_INCREMENT,
    justificacao TEXT,
    descricao TEXT,
    UNIQUE (justificacao (500))
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fundamentacao_contrato_dim (
    chave_fundamentacao INT PRIMARY KEY AUTO_INCREMENT,
    fundamentacao VARCHAR(255),
    descricao TEXT,
    UNIQUE (fundamentacao)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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

CREATE TABLE IF NOT EXISTS cpv_contratos_transf (
    id_contrato INT,
    cpv VARCHAR(10),
    cpv_descricao VARCHAR(255),
    UNIQUE (id_contrato, cpv)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS dim_entidade (
    chave_entidade INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS dim_detalhes_contratos (
    chave_contratos INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS dim_cpv_contratos (
    chave_contrato INT,
    chave_cpv INT,
    UNIQUE (chave_contrato, chave_cpv),
    PRIMARY KEY (chave_contrato, chave_cpv),
    FOREIGN KEY (chave_contrato) REFERENCES dim_detalhes_contratos (chave_contratos)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS dim_data (
    chave_date INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    feriado VARCHAR(100),
    fim_semana TINYINT(1),
    dia TINYINT,
    mes TINYINT,
    ano SMALLINT,
    dia_semana VARCHAR(20),
    mes_extenso VARCHAR(20),
    mes_abr VARCHAR(5),
    data_extenso VARCHAR(100),
    evento_natural VARCHAR(255),
    UNIQUE (data),
    UNIQUE (data_extenso)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fact_contratos (
    chave_contratos INT,
    adjudicante INT,
    chave_entidade INT,
    adjudicatario TINYINT(1),
    chave_tipo_contrato INT,
    chave_tipo_procedimento INT,
    chave_fundamentacao INT,
    chave_justificacao_nao_escrita INT,
    valor_contratual DECIMAL(15, 2),
    chave_data INT,
    PRIMARY KEY (
        chave_contratos,
        chave_entidade,
        adjudicante
    ),
    FOREIGN KEY (chave_contratos) REFERENCES dim_detalhes_contratos (chave_contratos),
    FOREIGN KEY (chave_entidade) REFERENCES dim_entidade (chave_entidade),
    FOREIGN KEY (chave_tipo_contrato) REFERENCES tipo_contrato_dim (chave_tipo_contrato),
    FOREIGN KEY (chave_tipo_procedimento) REFERENCES tipo_procedimento_dim (chave_tipo_procedimento),
    FOREIGN KEY (chave_fundamentacao) REFERENCES fundamentacao_contrato_dim (chave_fundamentacao),
    FOREIGN KEY (
        chave_justificacao_nao_escrita
    ) REFERENCES justificacao_contrato_nao_escrito_dim (chave_justificacao),
    FOREIGN KEY (chave_data) REFERENCES dim_data (chave_date)
);

-- =====================
-- INSERTS DOS VALORES NULOS
-- =====================

INSERT IGNORE INTO
    dim_entidade (
        id_entidade,
        nif,
        nome,
        total_adjudicatario,
        num_contratos_adjudicatario,
        total_adjudicante,
        num_contratos_adjudicante,
        pais
    )
VALUES (
        -1,
        NULL,
        'ENTIDADE INVALIDA',
        0,
        0,
        0,
        0,
        'N/A'
    );

INSERT IGNORE INTO
    dim_detalhes_contratos (
        id_contrato,
        objeto,
        descricao,
        data_publicacao,
        data_celebracao,
        valor_contratual,
        prazo_execucao,
        local_execucao,
        procedimento_centralizado,
        num_acordos_quadro,
        desc_acordo_quadro,
        data_fecho_contrato,
        valor_total_efetivo,
        regime,
        tipo_fim_contrato,
        crit_materiais,
        link_pecas,
        observacoes,
        contrato_ecologico,
        fundamentacao_ajuste_directo
    )
VALUES (
        -1,
        'N/A',
        'CONTRATO INVALIDO',
        NULL,
        NULL,
        0,
        0,
        'N/A',
        0,
        'N/A',
        'N/A',
        NULL,
        0,
        'N/A',
        'N/A',
        0,
        'N/A',
        'N/A',
        0,
        'N/A'
    );

INSERT IGNORE INTO
    dim_data (
        data,
        feriado,
        fim_semana,
        dia,
        mes,
        ano,
        dia_semana,
        mes_extenso,
        mes_abr,
        evento_natural,
        data_extenso
    )
VALUES (
        NULL,
        'N/A',
        NULL,
        NULL,
        NULL,
        NULL,
        'N/A',
        'N/A',
        'N/A',
        'N/A',
        'DATA INVALIDA'
    );

INSERT IGNORE INTO
    cpv_dim (
        codigo,
        cpv_descricao,
        descricao
    )
VALUES (
        'N/A',
        'N/A',
        'VALOR DESCONHECIDO'
    );

INSERT IGNORE INTO
    tipo_procedimento_dim (tipo, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO
    tipo_contrato_dim (tipo, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO
    justificacao_contrato_nao_escrito_dim (justificacao, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO
    fundamentacao_contrato_dim (fundamentacao, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

CREATE TABLE IF NOT EXISTS lookup_abreviaturas (
    abr VARCHAR(255),
    abr_correta VARCHAR(255)
);
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('L.D.A.','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('L. D. A.','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('LDA.','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('L.D.A','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('LD.ª','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('L.DA','LDA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('E.P.E.','EPE');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('E. P. E.','EPE');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('EPE.','EPE');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('E.P.E','EPE');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('S.A.','SA');
INSERT IGNORE INTO lookup_abreviaturas (abr, abr_correta) VALUES ('S.A','SA');

INSERT INTO terms (term, meaning) VALUES ('CPV', 'Vocabulário Comum para os Contratos Públicos - Sistema de classificação padronizado da União Europeia para identificar o objeto dos contratos públicos através de códigos.');
INSERT INTO terms (term, meaning) VALUES ('Entidade Adjudicante', 'A entidade pública ou organismo responsável por lançar o procedimento de contratação, definir as regras do concurso e adjudicar o contrato.');
INSERT INTO terms (term, meaning) VALUES ('Entidade Adjudicatária', 'O operador económico (empresa ou indivíduo) que venceu o concurso e a quem o contrato público foi formalmente atribuído.');
INSERT INTO terms (term, meaning) VALUES ('Procedimento', 'O conjunto de etapas formais e o enquadramento legal seguido para escolher um fornecedor (ex: Ajuste Direto, Concurso Público, Consulta Prévia).');
INSERT INTO terms (term, meaning) VALUES ('Tipo de Contrato', 'A classificação jurídica do contrato com base no seu objeto principal, como por exemplo: Empreitada de Obras Públicas, Aquisição de Bens ou Aquisição de Serviços.');
