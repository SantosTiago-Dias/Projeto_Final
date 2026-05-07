
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
    distrito                    VARCHAR(255),
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
    distrito                    VARCHAR(255),
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
    UNIQUE (data),
    UNIQUE (data_extenso)
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

INSERT IGNORE INTO dim_entidade (id_entidade, nif, nome, total_adjudicatario, num_contratos_adjudicatario, total_adjudicante, num_contratos_adjudicante, pais)
VALUES (-1, NULL, 'ENTIDADE INVALIDA', 0, 0, 0, 0, 'N/A');

INSERT IGNORE INTO dim_detalhes_contratos (id_contrato, objeto, descricao, data_publicacao, data_celebracao, valor_contratual, prazo_execucao,
    local_execucao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo,
    regime, tipo_fim_contrato, crit_materiais, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo)
VALUES (-1, 'N/A', 'CONTRATO INVALIDO', NULL, NULL, 0, 0, 'N/A', 0, 'N/A', 'N/A', NULL, 0, 'N/A', 'N/A', 0, 'N/A', 'N/A', 0, 'N/A');

INSERT IGNORE INTO dim_data (data, feriado, fim_semana, dia, mes, ano, dia_semana, nome_mes, abr_mes, evento_natural, data_extenso)
VALUES (NULL, 'N/A', NULL, NULL, NULL, NULL, 'N/A', 'N/A', 'N/A', 'N/A', 'DATA INVALIDA');

INSERT IGNORE INTO cpv_dictionary (codigo, cpv_descricao, descricao)
VALUES ('N/A', 'N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO tipo_procedimento_dictionary (tipo, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO tipo_contrato_dictionary (tipo, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO justificacao_contrato_nao_escrito_dictionary (justificacao, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

INSERT IGNORE INTO fundamentacao_contrato_dictionary (fundamentacao, descricao)
VALUES ('N/A', 'VALOR DESCONHECIDO');

CREATE TABLE IF NOT EXISTS lookup_abreviaturas(
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


-- ENTIDADES
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (246088, '600077594', 'Agrupamento de Escolas Alberto Sampaio, Braga', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3673, '-', 'Armando Peixoto de Sousa_Eurodidacta', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (38215, '501065962', 'Freguesia de Darque', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5649363, '-', 'Maria de Fátima Lopes da Costa Alves', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5649364, '-', 'Maria José dos Santos Azevedo Campainha Viana', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5649362, '-', 'Margarida Amorim Soares', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3934357, '515957631', 'Águas Públicas da Serra da Estrela, EIM, SA', 'Portugal,Guarda,Seia');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (412578, '510122639', 'AGR - Engenharia e Serviços, Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (1867, '505948605', 'Município de Guimarães', 'Portugal,Braga,Guimarães');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (38764, '500838909', 'Camacho Engenharia, S. A.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (1445, '501091823', 'Município de Felgueiras', 'Portugal,Porto,Felgueiras');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (2691653, '513843116', 'Transfodinamica Serviços para Eventos Unipessoal LDA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (175, '505387131', 'Município da Maia', 'Portugal,Porto,Maia');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (10067, '507701348', 'Joaquim Coelho da Silva, S.A.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (1037, '500025517', 'Sinop - António Moreira dos Santos, SA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3230, '506173968', 'Município do Seixal', 'Portugal,Setúbal,Seixal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (13319, '508190495', 'Alugal, Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3477, '501143530', 'Município de Castelo Branco', 'Portugal,Castelo Branco,Castelo Branco');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (312496, '509872069', 'ASSOCIAÇÃO PORTUGAL A MAO - Centro de Estudos e Promoção das Artes e Ofícios Portugueses', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (1265, '506833224', 'Município de Vila Real de Santo António', 'Portugal,Faro,Vila Real Sto Antonio');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5123533, '-', 'Sónia Maria Branco Fernandes', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3824, '500051070', 'Município de Lisboa', 'Portugal,Lisboa,Lisboa');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (117726, '508976669', 'Right Value Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (49038, '506676170', 'Município de Seia', 'Portugal,Guarda,Seia');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3340227, '515091944', 'Paulo Costa Garcia Unipessoal Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (823, '600012662', 'Ministério da Defesa Nacional - Marinha', 'Portugal,Lisboa,Lisboa');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (133401, '503576689', 'S.C.P.R. - Sociedade de Construção, Projetos e Reabilitação, Lda.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (144857, '504689878', 'CEIIA - Centro Exc. Inov. Ind. Automovel', 'Portugal,Porto,Matosinhos');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5083911, 'DE815636227', 'SEG Automotive Germany GmbH', 'Alemanha');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (681, '503494933', 'Instituto Politécnico do Cávado e do Ave', 'Portugal,Braga,Barcelos');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (11094, '502764406', 'Mbit - Computadores e Serviços de Informática SA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (3598390, '513960937', 'Páginas aos Blocos, Lda.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (4507514, '514746963', 'InevitableCode Uni. Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (637849, '513154990', 'Configbit - Soluções Tecnológicas, Unipessoal, Lda.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (2079826, '514360194', 'Megabarcelos - informática e tecnologia Unip.,Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (2342983, '514665637', 'MIXINFOR - SISTEMAS INFORMÁTICOS, UNIPESSOAL LDA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (4746226, '508194369', 'SOLUÇÕES BRILHANTES - EQUIPAMENTOS INFORMÁTICOS E RECICLAGEM UNIPESSOAL LDA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (1124, '504511270', 'Datagate - Desenvolvimento de Soluções Informáticas, Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5569, '503665410', 'Manuel Pedro de Sousa & Filhos, Lda', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (11391, '501461396', 'Protecnil - Sociedade Técnica de Construções, SA', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (13067, '500120501', 'Sanestradas-Empreitadas de Obras Públicas e Particulares, S.A.', 'Portugal');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (177, '505309939', 'Município de Portimão', 'Portugal,Faro,Portimão');
INSERT IGNORE INTO entidades_ext (id_entidade, nif, nome, pais) VALUES (5147433, '518603210', 'Pateo Marafado Associação Artistica e Cultural', 'Portugal');

-- CONTRATOS

INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686386, 'Aquisição de bens móveis', 'Consulta Prévia', 'AQUISIÇÃO DE MATERIAL DIDÁTICO - Pré-escolar e 1.º ciclo.', 'AQUISIÇÃO DE MATERIAL DIDÁTICO - Pré-escolar e 1.º ciclo.', '[{"nif": "600077594", "id": 246088, "description": "Agrupamento de Escolas Alberto Sampaio, Braga"}]', '28-04-2026', '28-04-2026', '4.404,08 €', '39162110-9', 'Material pedagógico', '260 dias', 'Portugal, Braga, Braga', 'Artigo 20.º, n.º 1, alínea c) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos ( DL 111-B/2017 )', 'Artigo 95.º, n.º 1, a), contrato de locação ou de aquisição de bens móveis ou de aquisição de serviços cujo preço contratual não excede 10.000,00 € e para Região Autónoma da Madeira um coeficiente de 1,45 €', NULL, '0', NULL, '[{"nif": "-", "id": 3673, "description": "Armando Peixoto de Sousa_Eurodidacta"}]', 'https://community.vortal.biz/Public/public-tender-documents/Z08vSHBudVVMZ3N2blY2dTEybHZKN05UeFp2Mzlpd2JQQVp5QXY3K09PQ08vdlN3V3graXJaVTk5T05zeUFYR0pZOC9PVEpsRmlWbkNFVlM5WlFFcFE9PXoobFVX', NULL, '0', 'Não aplicável');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686385, 'Aquisição de serviços', 'Consulta Prévia', 'Aquisição de serviços em regime de tarefa, para limpeza das ruas e jardinagem dos espaços verdes da Freguesia de Darque', 'Aquisição de serviços em regime de tarefa, para limpeza das ruas e jardinagem dos espaços verdes da Freguesia de Darque', '[{"nif": "501065962", "id": 38215, "description": "Freguesia de Darque"}]', '28-04-2026', '16-04-2026', '23.820,00 €', '90611000-3', 'Serviços de limpeza de ruas', '1006 dias', 'Portugal, Viana do Castelo, Viana do Castelo', 'Artigo 20.º, n.º 1, alínea c) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', '', NULL, '0', '[{"nif": "-", "id": 5649363, "description": "Maria de Fátima Lopes da Costa Alves"}, {"nif": "-", "id": 5649364, "description": "Maria José dos Santos Azevedo Campainha Viana"}, {"nif": "-", "id": 5649362, "description": "Margarida Amorim Soares"}]', '[{"nif": "-", "id": 5649363, "description": "Maria de Fátima Lopes da Costa Alves"}]', NULL, NULL, '0', 'Não aplicável');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686383, 'Aquisição de serviços', 'Consulta Prévia', 'Operação/Manutenção de ETAR e EEAR 2026', 'Operação/Manutenção de ETAR e EEAR 2026', '[{"nif": "515957631", "id": 3934357, "description": "Águas Públicas da Serra da Estrela, EIM, SA"}]', '28-04-2026', '17-04-2026', '24.000,00 €', '90400000-1', 'Serviços relacionados com águas residuais', '365 dias', 'Portugal', 'Artigo 20.º, n.º 1, alínea c) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos ( DL 111-B/2017 )', '', NULL, '0', '[{"nif": "510122639", "id": 412578, "description": "AGR - Engenharia e Serviços, Lda"}]', '[{"nif": "510122639", "id": 412578, "description": "AGR - Engenharia e Serviços, Lda"}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA3NDA0OQ', NULL, '0', 'Não aplicável');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686382, 'Empreitadas de obras públicas', 'Ajuste Direto Regime Geral', 'Execução de parque de estacionamento provisório na USF de Urgeses', 'Execução de parque de estacionamento provisório na USF de Urgeses', '[{"nif": "505948605", "id": 1867, "description": "Município de Guimarães"}]', '28-04-2026', '24-04-2026', '18.370,91 €', '45223300-9', 'Construção de parque de estacionamento', '30 dias', 'Portugal', 'Artigo 19.º, alínea d) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', '', NULL, '0', '[{"nif": "500838909", "id": 38764, "description": "Camacho Engenharia, S. A."}]', '[{"nif": "500838909", "id": 38764, "description": "Camacho Engenharia, S. A."}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA3NDA5Ng', NULL, '0', 'ausência de recursos próprios');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686380, 'Aquisição de serviços', 'Ajuste Direto Regime Geral', 'Aquisição de Serviços para Montagem de Estruturas e Organização Logística - "Feira de Maio 2026"', 'Aquisição de Serviços para Montagem de Estruturas e Organização Logística - "Feira de Maio 2026"', '[{"nif": "501091823", "id": 1445, "description": "Município de Felgueiras"}]', '28-04-2026', '28-04-2026', '10.000,00 €', '79952000-2', 'Serviços de eventos', '5 dias', 'Portugal', 'Artigo 20.º, n.º 1, alínea d) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', 'Artigo 95.º, n.º 1, c), locação ou aquisição de bens móveis ou de serviços nos termos das alíneas i),ii),iii),cumulativamente', NULL, '0', '[{"nif": "513843116", "id": 2691653, "description": "TRANSFODINAMICA SERVIÇOS PARA EVENTOS, UNIPESSOAL LDA"}]', '[{"nif": "513843116", "id": 2691653, "description": "Transfodinamica Serviços para Eventos Unipessoal LDA"}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA4NzIzOA', NULL, '0', 'ausência de recursos próprios');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686376, 'Empreitadas de obras públicas', 'Consulta Prévia', 'Substituição do lajeado de granito danificado na Praça Dr. José Vieira de Carvalho, na freguesia da Cidade da Maia', 'Substituição do lajeado de granito danificado na Praça Dr. José Vieira de Carvalho, na freguesia da Cidade da Maia', '[{"nif": "505387131", "id": 175, "description": "Município da Maia"}]', '28-04-2026', '27-03-2026', '39.997,75 €', '45262510-9', 'Obras em pedra', '75 dias', 'Portugal', 'Artigo 19.º, alínea c) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', '', NULL, '0', '[{"nif": "507701348", "id": 10067, "description": "Joaquim Coelho da Silva, S.A."}, {"nif": "500025517", "id": 1037, "description": "Sinop - António Moreira dos Santos, SA"}]', '[{"nif": "507701348", "id": 10067, "description": "Joaquim Coelho da Silva, S.A."}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTAwMjk4Mg', NULL, '0', 'Não aplicável');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686375, 'Aquisição de serviços', 'Consulta Prévia', 'Aluguer camarins e sanitários 25 Abril', 'Aluguer camarins e sanitários 25 Abril', '[{"nif": "506173968", "id": 3230, "description": "Município do Seixal"}]', '28-04-2026', '23-04-2026', '10.565,00 €', '79952000-2', 'Serviços de eventos', '8 dias', 'Portugal', 'Artigo 20.º, n.º 1, alínea c) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', 'Artigo 95.º, n.º 1, c), locação ou aquisição de bens móveis ou de serviços nos termos das alíneas i),ii),iii),cumulativamente', NULL, '0', '[{"nif": "508190495", "id": 13319, "description": "ALUGAL, LDA."}]', '[{"nif": "508190495", "id": 13319, "description": "Alugal, Lda"}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA3NzA4Mw', NULL, '0', 'Não aplicável');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686374, 'Aquisição de serviços', 'Ajuste Direto Regime Geral', 'Serviços para candidatar o Bordado de Castelo Branco à Inscrição na Lista Representativa do Património Cultural Imaterial da Humanidade  UNESCO.', 'Serviços para candidatar o Bordado de Castelo Branco à Inscrição na Lista Representativa do Património Cultural Imaterial da Humanidade  UNESCO.', '[{"nif": "501143530", "id": 3477, "description": "Município de Castelo Branco"}]', '28-04-2026', '28-04-2026', '19.850,00 €', '75112100-5', 'Serviços administrativos relacionados com projectos de desenvolvimento', '365 dias', 'Portugal', 'Artigo 20.º, n.º 1, alínea d) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', '', NULL, '0', '[{"nif": "509872069", "id": 312496, "description": "Associação Portugal à mão - Centro de Estudos e Promoção das Artes e Ofícios Portugueses"}]', '[{"nif": "509872069", "id": 312496, "description": "ASSOCIAÇÃO PORTUGAL A MAO - Centro de Estudos e Promoção das Artes e Ofícios Portugueses"}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA2NzI4OA', NULL, '0', 'ausência de recursos próprios');
INSERT IGNORE INTO contratos_ext (id_contrato, tipo_contrato, tipo_procedimento, objeto, descricao, adjudicante, data_publicacao, data_celebracao, valor_contratual, cpvs, cpvsDesignation, prazo_execucao, local_execucao, fundamentacao, procedimento_centralizado, num_acordos_quadro, desc_acordo_quadro, data_fecho_contrato, valor_total_efetivo, regime, justificacao_nao_escrita, tipo_fim_contrato, crit_materiais, concorrentes, adjudicatarios, link_pecas, observacoes, contrato_ecologico, fundamentacao_ajuste_directo) VALUES (14686373, 'Aquisição de serviços', 'Ajuste Direto Regime Geral', 'Prestação de Serviços, na Modalidade de Avença, para motorista de veículos pesados de passageiros', 'Prestação de Serviços, na Modalidade de Avença, para motorista de veículos pesados de passageiros', '[{"nif": "506833224", "id": 1265, "description": "Município de Vila Real de Santo António"}]', '28-04-2026', '28-04-2026', '10.800,00 €', '75100000-7', 'Serviços relacionados com a administração pública', '247 dias', 'Portugal', 'Artigo 20.º, n.º 1, alínea d) do Código dos Contratos Públicos', '0', 'Não aplicável.', 'Não aplicável.', NULL, NULL, 'Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05', '', NULL, '0', '[{"nif": "-", "id": 5123533, "description": "Sónia Maria Branco Fernandes"}]', '[{"nif": "-", "id": 5123533, "description": "Sónia Maria Branco Fernandes"}]', 'https://www.acingov.pt/acingovprod/2/zonaPublica/zona_publica_c/donwloadProcedurePiece/MTA3NzE0Ng', NULL, '0', 'ausência de recursos próprios');
