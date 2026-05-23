DROP FUNCTION IF EXISTS normalizar;

DELIMITER $$

CREATE FUNCTION normalizar(input TEXT)
    RETURNS TEXT
    DETERMINISTIC
BEGIN
    DECLARE result TEXT;

    IF input IS NULL OR input = '' THEN
        RETURN NULL;
    END IF;

    -- normalizar br
    SET result = REGEXP_REPLACE(input, '(?i)<br\\s*/?>', '; ');

    -- normalizar espaços múltiplos
    SET result = REGEXP_REPLACE(result, '\\s+', ' ');

    -- normalizar separadores duplicados
    SET result = REGEXP_REPLACE(result, '\\s*;\\s*', '; ');
    SET result = TRIM(result);

    RETURN result;
END$$

DELIMITER ;

DROP FUNCTION IF EXISTS normalizar_sc;

DELIMITER $$

CREATE FUNCTION normalizar_sc(input TEXT)
    RETURNS TEXT
    DETERMINISTIC
BEGIN
    DECLARE result TEXT;

    IF input IS NULL OR input = '' THEN
        RETURN NULL;
    END IF;

    SET result = input;


    SET result = REGEXP_REPLACE(
            result,
            ' C/ ?([[:alpha:]]{2,})',
            ' COM \\1'
                 );


    SET result = REGEXP_REPLACE(
            result,
            ' S/ ?([[:alpha:]]{2,})',
            ' SEM \\1'
                 );

    SET result = TRIM(result);

    RETURN result;
END$$

DELIMITER ;

DELIMITER $$

-- =============================================
-- TRANSFORM PROCEDURES
-- =============================================

DROP PROCEDURE IF EXISTS transform_detalhes_contratos$$

CREATE PROCEDURE transform_detalhes_contratos()
BEGIN

    INSERT IGNORE INTO detalhes_contratos_transf (
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
SELECT
    id_contrato,
    normalizar_sc(UPPER(normalizar(objeto))),
    normalizar_sc(UPPER(normalizar(descricao))),

    STR_TO_DATE(data_publicacao, '%d-%m-%Y'),
    STR_TO_DATE(data_celebracao, '%d-%m-%Y'),

    ABS(CAST(REPLACE(REPLACE(TRIM(TRAILING '€' FROM valor_contratual),'.', ''),',', '.') AS DECIMAL(15,2))),
    CAST(TRIM(REPLACE(prazo_execucao, ' dias', '')) AS UNSIGNED),

    UPPER(normalizar(local_execucao)),
    IF(procedimento_centralizado = 0, 'Não', 'Sim'),
    num_acordos_quadro,
    desc_acordo_quadro,

    STR_TO_DATE(data_fecho_contrato, '%d-%m-%Y'),

    CAST(REPLACE(REPLACE(TRIM(TRAILING '€' FROM valor_total_efetivo),'.', ''),',', '.') AS DECIMAL(15,2)),

    regime,

    IFNULL(tipo_fim_contrato, 'Não aplicável.'),

    IF(crit_materiais = 0, 'Não', 'Sim'),

    IFNULL(link_pecas, 'Não aplicável.'),
    IFNULL(observacoes, 'Não aplicável.'),

    IF(contrato_ecologico = 0, 'Não', 'Sim'),
    fundamentacao_ajuste_directo

FROM contratos_ext

    ON DUPLICATE KEY UPDATE
                         objeto = VALUES(objeto),
                         descricao = VALUES(descricao),
                         data_publicacao = VALUES(data_publicacao),
                         data_celebracao = VALUES(data_celebracao),
                         valor_contratual = VALUES(valor_contratual),
                         prazo_execucao = VALUES(prazo_execucao),
                         local_execucao = VALUES(local_execucao),
                         procedimento_centralizado = VALUES(procedimento_centralizado),
                         num_acordos_quadro = VALUES(num_acordos_quadro),
                         desc_acordo_quadro = VALUES(desc_acordo_quadro),
                         data_fecho_contrato = VALUES(data_fecho_contrato),
                         valor_total_efetivo = VALUES(valor_total_efetivo),
                         regime = VALUES(regime),
                         tipo_fim_contrato = VALUES(tipo_fim_contrato),
                         crit_materiais = VALUES(crit_materiais),
                         link_pecas = VALUES(link_pecas),
                         observacoes = VALUES(observacoes),
                         contrato_ecologico = VALUES(contrato_ecologico),
                         fundamentacao_ajuste_directo = VALUES(fundamentacao_ajuste_directo);

END$$

DROP PROCEDURE IF EXISTS transform_contratos$$

CREATE PROCEDURE transform_contratos()
BEGIN

    -- =========================
    -- ADJUDICATÁRIOS
    -- =========================
INSERT INTO contratos_transf (
    id_contrato,
    id_entidade,
    adjudicatario,
    tipo_contrato,
    tipo_procedimento,
    fundamentacao,
    justificacao_nao_escrita,
    id_adjudicante
)
SELECT
    c.id_contrato,

    JSON_UNQUOTE(JSON_EXTRACT(a.value, '$.id')) AS id_entidade,

    1 AS adjudicatario,

    (
        SELECT GROUP_CONCAT(TRIM(jt.val) ORDER BY TRIM(jt.val) SEPARATOR ', ')
        FROM JSON_TABLE(
                     CONCAT(
                             '["',
                             REPLACE(REPLACE(c.tipo_contrato, '<br/>', ','), ',', '","'),
                             '"]'
                     ),
                     '$[*]' COLUMNS (
                         val VARCHAR(255) PATH '$'
                         )
             ) jt
    ),
    normalizar(c.tipo_procedimento),
    c.fundamentacao,
    c.justificacao_nao_escrita,

    JSON_UNQUOTE(JSON_EXTRACT(c.adjudicante, '$[0].id')) AS id_adjudicante

FROM contratos_ext c

         JOIN JSON_TABLE(c.adjudicatarios, '$[*]'
    COLUMNS (value JSON PATH '$')
              ) a ON TRUE

         LEFT JOIN tipo_contrato_dictionary tc
                   ON tc.tipo = c.tipo_contrato

         LEFT JOIN tipo_procedimento_dictionary tp
                   ON tp.tipo = c.tipo_procedimento

         LEFT JOIN fundamentacao_contrato_dictionary f
                   ON f.fundamentacao = c.fundamentacao

         LEFT JOIN justificacao_contrato_nao_escrito_dictionary j
                   ON j.justificacao = c.justificacao_nao_escrita

    ON DUPLICATE KEY UPDATE
                         id_adjudicante = VALUES(id_adjudicante),
                         tipo_contrato = VALUES(tipo_contrato),
                         tipo_procedimento = VALUES(tipo_procedimento),
                         fundamentacao = VALUES(fundamentacao),
                         justificacao_nao_escrita = VALUES(justificacao_nao_escrita);


-- =========================
-- CONCORRENTES
-- =========================
INSERT INTO contratos_transf (
    id_contrato,
    id_entidade,
    adjudicatario,
    tipo_contrato,
    tipo_procedimento,
    fundamentacao,
    justificacao_nao_escrita,
    id_adjudicante
)
SELECT
    c.id_contrato,

    JSON_UNQUOTE(JSON_EXTRACT(co.value, '$.id')) AS id_entidade,

    0 AS adjudicatario,

    (
        SELECT GROUP_CONCAT(TRIM(jt.val) ORDER BY TRIM(jt.val) SEPARATOR ', ')
        FROM JSON_TABLE(
                     CONCAT(
                             '["',
                             REPLACE(REPLACE(c.tipo_contrato, '<br/>', ','), ',', '","'),
                             '"]'
                     ),
                     '$[*]' COLUMNS (
                         val VARCHAR(255) PATH '$'
                         )
             ) jt
    ),
    normalizar(c.tipo_procedimento),
    c.fundamentacao,
    c.justificacao_nao_escrita,

    JSON_UNQUOTE(JSON_EXTRACT(c.adjudicante, '$[0].id')) AS id_adjudicante

FROM contratos_ext c

         JOIN JSON_TABLE(c.concorrentes, '$[*]'
    COLUMNS (value JSON PATH '$')
              ) co ON TRUE

         LEFT JOIN tipo_contrato_dictionary tc
                   ON tc.tipo = c.tipo_contrato

         LEFT JOIN tipo_procedimento_dictionary tp
                   ON tp.tipo = c.tipo_procedimento

         LEFT JOIN fundamentacao_contrato_dictionary f
                   ON f.fundamentacao = c.fundamentacao

         LEFT JOIN justificacao_contrato_nao_escrito_dictionary j
                   ON j.justificacao = c.justificacao_nao_escrita

WHERE NOT EXISTS (
    SELECT 1
    FROM contratos_transf ct2
    WHERE ct2.id_contrato = c.id_contrato
      AND ct2.adjudicatario = 1
      AND ct2.id_entidade = JSON_UNQUOTE(JSON_EXTRACT(co.value, '$.id'))
)

    ON DUPLICATE KEY UPDATE
                         id_adjudicante = VALUES(id_adjudicante),
                         tipo_contrato = VALUES(tipo_contrato),
                         tipo_procedimento = VALUES(tipo_procedimento),
                         fundamentacao = VALUES(fundamentacao),
                         justificacao_nao_escrita = VALUES(justificacao_nao_escrita);

END$$

DROP PROCEDURE IF EXISTS transform_entidades$$

CREATE PROCEDURE transform_entidades()
BEGIN

INSERT INTO entidade_transf (
    id_entidade,
    nif,
    nome,
    pais,
    distrito,
    total_adjudicatario,
    num_contratos_adjudicatario,
    total_adjudicante,
    num_contratos_adjudicante
)
SELECT
    e.id_entidade,
    e.nif,
    UPPER(TRIM(e.nome)),
    IFNULL(e.pais, 'N/A'),
    'N/A',
    0, 0, 0, 0

FROM entidades_ext e
         LEFT JOIN entidade_transf t
                   ON e.id_entidade = t.id_entidade

WHERE t.id_entidade IS NULL
    ON DUPLICATE KEY UPDATE
                         nif = VALUES(nif),
                         nome = VALUES(nome),
                         pais = VALUES(pais);

-- Metricas para adjudicatários
UPDATE entidade_transf t
    JOIN (
    SELECT
    ct.id_entidade,
    COUNT(DISTINCT ct.id_contrato) AS num_contratos,
    SUM(dc.valor_contratual) AS total_valor

    FROM contratos_transf ct
    JOIN detalhes_contratos_transf dc
    ON ct.id_contrato = dc.id_contrato

    WHERE ct.adjudicatario = 1
    GROUP BY ct.id_entidade
    ) agg
ON t.id_entidade = agg.id_entidade
    SET
        t.num_contratos_adjudicatario =IFNULL(agg.num_contratos,0),
        t.total_adjudicatario =IFNULL(agg.total_valor,0);

-- Metricas para adjudicantes
UPDATE entidade_transf t
    JOIN (
    SELECT
    ct.id_adjudicante AS id_entidade,
    COUNT(DISTINCT ct.id_contrato) AS num_contratos,
    SUM(dc.valor_contratual) AS total_valor

    FROM contratos_transf ct
    JOIN detalhes_contratos_transf dc
    ON ct.id_contrato = dc.id_contrato

    WHERE ct.id_adjudicante IS NOT NULL
    GROUP BY ct.id_adjudicante
    ) agg
ON t.id_entidade = agg.id_entidade
    SET
        t.num_contratos_adjudicante = IFNULL(t.num_contratos_adjudicante,0) + IFNULL(agg.num_contratos,0),
        t.total_adjudicante = IFNULL(t.total_adjudicante,0) + IFNULL(agg.total_valor,0);


END$$

DROP PROCEDURE IF EXISTS transform_cpv_contratos$$

CREATE PROCEDURE transform_cpv_contratos()
BEGIN

    INSERT IGNORE INTO cpv_contratos_transf (id_contrato, cpv, cpv_descricao)
SELECT
    c.id_contrato,
    TRIM(cpv.value) AS cpv,
    TRIM(descp.value) AS cpv_descricao

FROM contratos_ext c

         JOIN JSON_TABLE(CONCAT('["', REPLACE(REPLACE(IFNULL(c.cpvs, ''), ' | ', '|'), '|', '","'), '"]'),
                         "$[*]" COLUMNS (value VARCHAR(50) PATH "$",ord FOR ORDINALITY)) cpv

         JOIN JSON_TABLE(CONCAT('["',REPLACE(REPLACE(IFNULL(c.cpvsDesignation, ''), ' | ', '|'), '|', '","'),'"]'),
                         "$[*]" COLUMNS (value VARCHAR(255) PATH "$",ord FOR ORDINALITY)) descp
              ON cpv.ord = descp.ord

    WHERE NULLIF(TRIM(cpv.value), '') IS NOT NULL;

END$$

DROP PROCEDURE IF EXISTS normalizar_lookup;

DELIMITER $$

CREATE PROCEDURE normalizar_lookup(
    IN p_table VARCHAR(100),
    IN p_column VARCHAR(100)
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_abr VARCHAR(100);
    DECLARE v_corr VARCHAR(100);

    DECLARE cur CURSOR FOR
        SELECT abr, abr_correta FROM lookup_abreviaturas;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_abr, v_corr;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @v_abr = v_abr;
        SET @v_corr = v_corr;

        SET @sql = CONCAT(
            'UPDATE ', p_table, '
             SET ', p_column, ' = REPLACE(', p_column, ', ?, ?)
             WHERE ', p_column, ' LIKE CONCAT("%", ?, "%")'
        );

        PREPARE stmt FROM @sql;
        EXECUTE stmt USING @v_abr, @v_corr, @v_abr;
        DEALLOCATE PREPARE stmt;

    END LOOP;

    CLOSE cur;
END$$


-- =============================================
-- LOAD PROCEDURES
-- =============================================

DROP PROCEDURE IF EXISTS load_dim_entidade$$

CREATE PROCEDURE load_dim_entidade () BEGIN

INSERT INTO
    dim_entidade (
        id_entidade,
        nif,
        nome,
        total_adjudicatario,
        num_contratos_adjudicatario,
        total_adjudicante,
        num_contratos_adjudicante,
        pais,
        distrito
    )
SELECT e.id_entidade, e.nif, e.nome, e.total_adjudicatario, e.num_contratos_adjudicatario, e.total_adjudicante, e.num_contratos_adjudicante, e.pais, e.distrito
FROM entidade_transf e
WHERE
    NOT EXISTS (
        SELECT 1
        FROM dim_entidade d
        WHERE
            d.id_entidade = e.id_entidade
    );

END $$

DROP PROCEDURE IF EXISTS load_dim_detalhes_contratos$$

CREATE PROCEDURE load_dim_detalhes_contratos () BEGIN

INSERT INTO
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
SELECT
    d.id_contrato,
    d.objeto,
    d.descricao,
    d.data_publicacao,
    d.data_celebracao,
    d.valor_contratual,
    d.prazo_execucao,
    d.local_execucao,
    d.procedimento_centralizado,
    d.num_acordos_quadro,
    d.desc_acordo_quadro,
    d.data_fecho_contrato,
    d.valor_total_efetivo,
    d.regime,
    d.tipo_fim_contrato,
    d.crit_materiais,
    d.link_pecas,
    d.observacoes,
    d.contrato_ecologico,
    d.fundamentacao_ajuste_directo
FROM detalhes_contratos_transf d
ON DUPLICATE KEY UPDATE
    objeto = VALUES(objeto),
    descricao = VALUES(descricao),
    data_publicacao = VALUES(data_publicacao),
    data_celebracao = VALUES(data_celebracao),
    valor_contratual = VALUES(valor_contratual),
    prazo_execucao = VALUES(prazo_execucao),
    local_execucao = VALUES(local_execucao),
    procedimento_centralizado = VALUES(procedimento_centralizado),
    num_acordos_quadro = VALUES(num_acordos_quadro),
    desc_acordo_quadro = VALUES(desc_acordo_quadro),
    data_fecho_contrato = VALUES(data_fecho_contrato),
    valor_total_efetivo = VALUES(valor_total_efetivo),
    regime = VALUES(regime),
    tipo_fim_contrato = VALUES(tipo_fim_contrato),
    crit_materiais = VALUES(crit_materiais),
    link_pecas = VALUES(link_pecas),
    observacoes = VALUES(observacoes),
    contrato_ecologico = VALUES(contrato_ecologico),
    fundamentacao_ajuste_directo = VALUES(fundamentacao_ajuste_directo);

END $$

DROP PROCEDURE IF EXISTS load_dim_cpv_contratos$$

CREATE PROCEDURE load_dim_cpv_contratos () BEGIN

INSERT IGNORE INTO
    dim_cpv_contratos (chave_contrato, chave_cpv)
SELECT dc.chave_contratos, cp.id_cpv AS chave_cpv
FROM
    cpv_contratos_transf c
    INNER JOIN dim_detalhes_contratos dc ON dc.id_contrato = c.id_contrato
    INNER JOIN cpv_dictionary cp ON cp.codigo = c.cpv;

END $$

DROP PROCEDURE IF EXISTS load_dim_data$$

CREATE PROCEDURE load_dim_data (
    IN data_inicio DATE,
    IN data_fim DATE
) BEGIN DECLARE d DATE;

DECLARE Ano INT;
    DECLARE a INT; DECLARE b INT; DECLARE c INT;
    DECLARE d1 INT; DECLARE e INT; DECLARE f INT;
    DECLARE g INT; DECLARE h INT; DECLARE i INT;
    DECLARE k INT; DECLARE l INT; DECLARE m INT;

    DECLARE MesPascoa INT;
    DECLARE DiaPascoa INT;
    DECLARE Pascoa DATE;

    SET d = data_inicio;

    WHILE d <= data_fim DO

        SET Ano = YEAR(d);

        -- Algoritmo da Páscoa (igual ao DAX)
        SET a = MOD(Ano,19);
        SET b = FLOOR(Ano/100);
        SET c = MOD(Ano,100);
        SET d1 = FLOOR(b/4);
        SET e = MOD(b,4);
        SET f = FLOOR((b+8)/25);
        SET g = FLOOR((b-f+1)/3);
        SET h = MOD(19*a + b - d1 - g + 15,30);
        SET i = FLOOR(c/4);
        SET k = MOD(c,4);
        SET l = MOD(32 + 2*e + 2*i - h - k,7);
        SET m = FLOOR((a + 11*h + 22*l)/451);

        SET MesPascoa = FLOOR((h + l - 7*m + 114)/31);
        SET DiaPascoa = MOD(h + l - 7*m + 114,31) + 1;

        SET Pascoa = STR_TO_DATE(CONCAT(Ano,'-',MesPascoa,'-',DiaPascoa),'%Y-%m-%d');

INSERT INTO dim_data (
    data,
    feriado,
    fim_semana,
    dia,
    mes,
    ano,
    dia_semana,
    mes_extenso,
    mes_abr,
    data_extenso
)
VALUES (
           d,

           CASE
               -- Fixos
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-01-01'),'%Y-%m-%d') THEN 'Ano Novo'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-04-25'),'%Y-%m-%d') THEN 'Dia da Liberdade'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-05-01'),'%Y-%m-%d') THEN 'Dia do Trabalhador'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-06-10'),'%Y-%m-%d') THEN 'Dia de Portugal'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-08-15'),'%Y-%m-%d') THEN 'Assunção'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-10-05'),'%Y-%m-%d') THEN 'Implantação da República'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-11-01'),'%Y-%m-%d') THEN 'Todos os Santos'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-12-01'),'%Y-%m-%d') THEN 'Restauração da Independência'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-12-08'),'%Y-%m-%d') THEN 'Imaculada Conceição'
               WHEN d = STR_TO_DATE(CONCAT(Ano,'-12-25'),'%Y-%m-%d') THEN 'Natal'

               -- Móveis
               WHEN d = DATE_SUB(Pascoa, INTERVAL 47 DAY) THEN 'Carnaval'
               WHEN d = DATE_SUB(Pascoa, INTERVAL 2 DAY) THEN 'Sexta-feira Santa'
               WHEN d = Pascoa THEN 'Páscoa'
               WHEN d = DATE_ADD(Pascoa, INTERVAL 60 DAY) THEN 'Corpo de Deus'

               ELSE 'Não aplicável.'
               END

,

-- fim de semana
CASE
    WHEN DAYOFWEEK(d) IN (1, 7) THEN 1
    ELSE 0
END,
DAY(d),
MONTH(d),
YEAR(d),

-- dia semana
CASE DAYOFWEEK(d)
    WHEN 1 THEN 'domingo'
    WHEN 2 THEN 'segunda-feira'
    WHEN 3 THEN 'terça-feira'
    WHEN 4 THEN 'quarta-feira'
    WHEN 5 THEN 'quinta-feira'
    WHEN 6 THEN 'sexta-feira'
    WHEN 7 THEN 'sábado'
END,

-- mês nome
CASE MONTH(d)
    WHEN 1 THEN 'janeiro'
    WHEN 2 THEN 'fevereiro'
    WHEN 3 THEN 'março'
    WHEN 4 THEN 'abril'
    WHEN 5 THEN 'maio'
    WHEN 6 THEN 'junho'
    WHEN 7 THEN 'julho'
    WHEN 8 THEN 'agosto'
    WHEN 9 THEN 'setembro'
    WHEN 10 THEN 'outubro'
    WHEN 11 THEN 'novembro'
    WHEN 12 THEN 'dezembro'
END,

-- abreviação
CASE MONTH(d)
    WHEN 1 THEN 'jan'
    WHEN 2 THEN 'fev'
    WHEN 3 THEN 'mar'
    WHEN 4 THEN 'abr'
    WHEN 5 THEN 'mai'
    WHEN 6 THEN 'jun'
    WHEN 7 THEN 'jul'
    WHEN 8 THEN 'ago'
    WHEN 9 THEN 'set'
    WHEN 10 THEN 'out'
    WHEN 11 THEN 'nov'
    WHEN 12 THEN 'dez'
END,

-- data extenso
CONCAT(
                DAY(d), ' de ',
                CASE MONTH(d)
                    WHEN 1 THEN 'janeiro'
                    WHEN 2 THEN 'fevereiro'
                    WHEN 3 THEN 'março'
                    WHEN 4 THEN 'abril'
                    WHEN 5 THEN 'maio'
                    WHEN 6 THEN 'junho'
                    WHEN 7 THEN 'julho'
                    WHEN 8 THEN 'agosto'
                    WHEN 9 THEN 'setembro'
                    WHEN 10 THEN 'outubro'
                    WHEN 11 THEN 'novembro'
                    WHEN 12 THEN 'dezembro'
                END,
                ' de ', YEAR(d)
            )
        );

SET d = DATE_ADD(d, INTERVAL 1 DAY);

END WHILE;

END $$

DROP PROCEDURE IF EXISTS load_fact$$

CREATE PROCEDURE load_fact () BEGIN

INSERT INTO
    fact_contratos (
        chave_contratos,
        chave_entidade,
        adjudicatario,
        chave_tipo_contrato,
        chave_tipo_procedimento,
        chave_fundamentacao,
        chave_justificacao_nao_escrita,
        adjudicante,
        valor_contratual,
        chave_data
    )
SELECT COALESCE(
        dc.chave_contratos, (
            SELECT chave_contratos
            FROM dim_detalhes_contratos
            WHERE
                id_contrato = -1
        )
    ), COALESCE(
        de.chave_entidade, (
            SELECT chave_entidade
            FROM dim_entidade
            WHERE
                id_entidade = -1
        )
    ), ct.adjudicatario, COALESCE(
        tc.chave_tipo_contrato, (
            SELECT chave_tipo_contrato
            FROM tipo_contrato_dim
            WHERE
                tipo = 'N/A'
        )
    ), COALESCE(
        tp.chave_tipo_procedimento, (
            SELECT chave_tipo_procedimento
            FROM tipo_procedimento_dim
            WHERE
                tipo = 'N/A'
        )
    ), COALESCE(
        fc.chave_fundamentacao, (
            SELECT chave_fundamentacao
            FROM fundamentacao_contrato_dim
            WHERE
                fundamentacao = 'N/A'
        )
    ), COALESCE(
        jc.chave_justificacao, (
            SELECT chave_justificacao
            FROM
                justificacao_contrato_nao_escrito_dim
            WHERE
                justificacao = 'N/A'
        )
    ), COALESCE(
        deadjudicante.chave_entidade, (
            SELECT chave_entidade
            FROM dim_entidade
            WHERE
                id_entidade = -1
        )
    ), dc.valor_contratual, COALESCE(
        dd.chave_date, (
            SELECT chave_date
            FROM dim_data
            WHERE
                data IS NULL
        )
    )
FROM
    contratos_transf ct
    LEFT JOIN dim_detalhes_contratos dc ON dc.id_contrato = ct.id_contrato
    LEFT JOIN dim_entidade de ON de.id_entidade = ct.id_entidade
    LEFT JOIN dim_entidade deadjudicante ON deadjudicante.id_entidade = ct.id_adjudicante
    LEFT JOIN tipo_contrato_dim tc ON tc.tipo = ct.tipo_contrato
    LEFT JOIN tipo_procedimento_dim tp ON tp.tipo = ct.tipo_procedimento
    LEFT JOIN fundamentacao_contrato_dim fc ON fc.fundamentacao = ct.fundamentacao
    LEFT JOIN justificacao_contrato_nao_escrito_dim jc ON jc.justificacao = ct.justificacao_nao_escrita
    LEFT JOIN dim_data dd ON dd.data = dc.data_celebracao
ON DUPLICATE KEY UPDATE
    adjudicatario = VALUES(adjudicatario),
    chave_tipo_contrato = VALUES(chave_tipo_contrato),
    chave_tipo_procedimento = VALUES(chave_tipo_procedimento),
    chave_fundamentacao = VALUES(chave_fundamentacao),
    chave_justificacao_nao_escrita = VALUES(
        chave_justificacao_nao_escrita
    ),
    valor_contratual = VALUES(valor_contratual),
    chave_data = VALUES(chave_data);

END $$

DROP PROCEDURE IF EXISTS load_dims_dict$$

CREATE PROCEDURE load_dims_dict () BEGIN
-- Tipo Contrato
INSERT IGNORE INTO
    tipo_contrato_dim (tipo, descricao)
SELECT DISTINCT
    tipo,
    descricao
FROM tipo_contrato_dictionary;

-- Tipo Procedimento
INSERT IGNORE INTO
    tipo_procedimento_dim (tipo, descricao)
SELECT DISTINCT
    tipo,
    descricao
FROM tipo_procedimento_dictionary;

-- Fundamentação Contrato
INSERT IGNORE INTO
    fundamentacao_contrato_dim (fundamentacao, descricao)
SELECT DISTINCT
    fundamentacao,
    descricao
FROM
    fundamentacao_contrato_dictionary;

-- Justificação Contrato Não Escrito
INSERT IGNORE INTO
    justificacao_contrato_nao_escrito_dim (justificacao, descricao)
SELECT DISTINCT
    justificacao,
    descricao
FROM
    justificacao_contrato_nao_escrito_dictionary;

-- CPV
INSERT IGNORE INTO
    cpv_dim (codigo, descricao)
SELECT DISTINCT
    codigo,
    descricao
FROM cpv_dictionary;

END $$