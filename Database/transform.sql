
DELIMITER $$

CREATE PROCEDURE transform_detalhes_contratos()
BEGIN

    INSERT IGNORE INTO DETALHES_CONTRATOS_TRANSF (
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
        objeto,
        descricao,

        STR_TO_DATE(data_publicacao, '%d-%m-%Y'),
        STR_TO_DATE(data_celebracao, '%d-%m-%Y'),

        IFNULL(CAST(REPLACE(REPLACE(TRIM(TRAILING '€' FROM valor_contratual),'.', ''),',', '.') AS DECIMAL(15,2)),0),
        IFNULL(CAST(TRIM(REPLACE(prazo_execucao, ' dias', '')) AS UNSIGNED),0),

        local_execucao,
        procedimento_centralizado,
        num_acordos_quadro,
        desc_acordo_quadro,

        STR_TO_DATE(data_fecho_contrato, '%d-%m-%Y'),

        IFNULL(CAST(REPLACE(REPLACE(TRIM(TRAILING '€' FROM valor_total_efetivo),'.', ''),',', '.') AS DECIMAL(15,2)),0),

        regime,

        IFNULL(tipo_fim_contrato, 'Não Aplicável'),

        crit_materiais,

        IFNULL(link_pecas, 'Não Aplicável'),
        IFNULL(observacoes, 'Não Aplicável'),

        contrato_ecologico,
        fundamentacao_ajuste_directo

    FROM contratos_ext;

END$$

DELIMITER $$

CREATE PROCEDURE transform_contratos()
BEGIN

    -- =========================
    -- ADJUDICATÁRIOS
    -- =========================
    INSERT INTO contratos_transf (
        id_contrato,
        id_entidade,
        adjudicatario,
        chave_tipo_contrato,
        chave_tipo_procedimento,
        -- chave_fundamentacao,
        chave_justificacao_nao_escrita,
        id_adjudicante
    )
    SELECT 
        c.id_contrato,

        JSON_UNQUOTE(JSON_EXTRACT(a.value, '$.id')) AS id_entidade,

        1 AS adjudicatario,

        tc.id_tipo_contrato AS chave_tipo_contrato,
        tp.id_tipo_procedimento AS chave_tipo_procedimento,
        -- f.id_fundamentacao AS chave_fundamentacao,
        j.id_justificacao AS chave_justificacao_nao_escrita,

        JSON_UNQUOTE(JSON_EXTRACT(c.adjudicante, '$[0].id')) AS id_adjudicante

    FROM contratos_ext c

    JOIN JSON_TABLE(c.adjudicatarios, '$[*]' 
        COLUMNS (value JSON PATH '$')
    ) a ON TRUE

    LEFT JOIN tipo_contrato_dictionary_ext tc 
        ON tc.tipo = c.tipo_contrato

    LEFT JOIN tipo_procedimento_dictionary_ext tp 
        ON tp.tipo = c.tipo_procedimento

    -- LEFT JOIN fundamentacao_contrato_dictionary_ext f 
        -- ON f.fundamentacao = c.fundamentacao

    LEFT JOIN justificacao_contrato_nao_escrito_dictionary_ext j 
        ON j.justificacao = c.justificacao_nao_escrita

    ON DUPLICATE KEY UPDATE 
        chave_tipo_contrato = VALUES(chave_tipo_contrato),
        chave_tipo_procedimento = VALUES(chave_tipo_procedimento),
        -- chave_fundamentacao = VALUES(chave_fundamentacao),
        chave_justificacao_nao_escrita = VALUES(chave_justificacao_nao_escrita),
        id_adjudicante = VALUES(id_adjudicante);


    -- =========================
    -- CONCORRENTES
    -- =========================
    INSERT INTO contratos_transf (
        id_contrato,
        id_entidade,
        adjudicatario,
        chave_tipo_contrato,
        chave_tipo_procedimento,
        -- chave_fundamentacao,
        chave_justificacao_nao_escrita,
        id_adjudicante
    )
    SELECT 
        c.id_contrato,

        JSON_UNQUOTE(JSON_EXTRACT(co.value, '$.id')) AS id_entidade,

        0 AS adjudicatario,

        tc.id_tipo_contrato AS chave_tipo_contrato,
        tp.id_tipo_procedimento AS chave_tipo_procedimento,
        -- f.id_fundamentacao AS chave_fundamentacao,
        j.id_justificacao AS chave_justificacao_nao_escrita,

        JSON_UNQUOTE(JSON_EXTRACT(c.adjudicante, '$[0].id')) AS id_adjudicante

    FROM contratos_ext c

    JOIN JSON_TABLE(c.concorrentes, '$[*]' 
        COLUMNS (value JSON PATH '$')
    ) co ON TRUE

    LEFT JOIN tipo_contrato_dictionary_ext tc 
        ON tc.tipo = c.tipo_contrato

    LEFT JOIN tipo_procedimento_dictionary_ext tp 
        ON tp.tipo = c.tipo_procedimento

    -- LEFT JOIN fundamentacao_contrato_dictionary_ext f 
        -- ON f.fundamentacao = c.fundamentacao

    LEFT JOIN justificacao_contrato_nao_escrito_dictionary_ext j 
        ON j.justificacao = c.justificacao_nao_escrita

    WHERE JSON_UNQUOTE(JSON_EXTRACT(co.value, '$.id')) NOT IN (
        SELECT id_entidade 
        FROM contratos_transf 
        WHERE id_contrato = c.id_contrato 
          AND adjudicatario = 1
    )

    ON DUPLICATE KEY UPDATE 
        chave_tipo_contrato = VALUES(chave_tipo_contrato),
        chave_tipo_procedimento = VALUES(chave_tipo_procedimento),
        -- chave_fundamentacao = VALUES(chave_fundamentacao),
        chave_justificacao_nao_escrita = VALUES(chave_justificacao_nao_escrita),
        id_adjudicante = VALUES(id_adjudicante);

END$$

DELIMITER ;

CREATE PROCEDURE transform_entidades()
BEGIN

    INSERT INTO entidade_transf (
        id_entidade,
        nif,
        nome,
        pais,
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
        0, 0, 0, 0

    FROM entidades_ext e
    LEFT JOIN entidade_transf t
        ON e.id_entidade = t.id_entidade

    WHERE t.id_entidade IS NULL;

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

    WHERE TRIM(cpv.value) <> '';

END$$

DELIMITER ;


CALL transform_detalhes_contratos();
CALL transform_contratos();
CALL transform_entidades();
CALL transform_cpv_contratos();