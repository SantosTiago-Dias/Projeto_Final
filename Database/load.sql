DELIMITER $$

CREATE PROCEDURE load_dim_entidade()
BEGIN
    INSERT INTO dim_entidade (
        id_entidade,
        nif,
        nome,
        total_adjudicatario,
        num_contratos_adjudicatario,
        total_adjudicante,
        num_contratos_adjudicante,
        pais
    )
    SELECT 
        e.id_entidade,
        e.nif,
        e.nome,
        e.total_adjudicatario,
        e.num_contratos_adjudicatario,
        e.total_adjudicante,
        e.num_contratos_adjudicante,
        e.pais

    FROM entidade_transf e
    WHERE NOT EXISTS (
        SELECT 1 
        FROM dim_entidade d 
        WHERE d.id_entidade = e.id_entidade
    );

END$$

CREATE PROCEDURE load_dim_detalhes_contratos()
BEGIN
    INSERT INTO dim_detalhes_contratos (
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

    WHERE NOT EXISTS (
        SELECT 1 
        FROM dim_detalhes_contratos dc
        WHERE dc.id_contrato = d.id_contrato
    );
END$$

CREATE PROCEDURE load_dim_cpv_contratos()
BEGIN
    INSERT INTO dim_cpv_contratos (chave_contrato, cpv)
    SELECT dc.chave_contratos, c.cpv

    FROM cpv_contratos_transf c

    INNER JOIN dim_detalhes_contratos dc 
        ON dc.id_contrato = c.id_contrato

    WHERE NOT EXISTS (
        SELECT 1 
        FROM dim_cpv_contratos d
        WHERE d.chave_contrato = dc.chave_contratos
          AND d.cpv = c.cpv
    );
END$$

CREATE PROCEDURE load_fact()
BEGIN
    INSERT INTO fact_contratos (
        chave_contratos,
        chave_entidade,
        adjudicatario,
        chave_tipo_contrato,
        chave_tipo_procedimento,
        chave_fundamentacao,
        chave_justificacao_nao_escrita,
        adjudicante,
        valor_contratual,
        data_celebracao
    )
    SELECT 
        dc.chave_contratos,
        de.chave_entidade,
        ct.adjudicatario,
        ct.chave_tipo_contrato,
        ct.chave_tipo_procedimento,
        ct.chave_fundamentacao,
        ct.chave_justificacao_nao_escrita,
        deadjudicante.chave_entidade AS adjudicante,

        dc.valor_contratual,
        dc.data_celebracao

    FROM contratos_transf ct

    INNER JOIN dim_detalhes_contratos dc 
        ON dc.id_contrato = ct.id_contrato

    LEFT JOIN dim_entidade de 
        ON de.id_entidade = ct.id_entidade
    
    LEFT JOIN dim_entidade deadjudicante
        ON deadjudicante.id_entidade = ct.id_adjudicante 

    WHERE NOT EXISTS (
        SELECT 1
        FROM fact_contratos f
        WHERE f.chave_contratos = dc.chave_contratos
          AND f.chave_entidade = de.chave_entidade
          AND f.adjudicatario = ct.adjudicatario
    );

END$$

DELIMITER ;

CALL load_dim_entidade();
CALL load_dim_detalhes_contratos();
CALL load_dim_cpv_contratos();
CALL load_fact();