DROP VIEW IF EXISTS view_contratos_maior_valor;
DROP VIEW IF EXISTS view_contratos_menor_valor;
DROP VIEW IF EXISTS view_entidades_mais_contratos_adjudicados;
DROP VIEW IF EXISTS view_entidades_mais_concorrem_menos_ganham;

CREATE VIEW  view_contratos_maior_valor AS
    SELECT chave_contratos,objeto,valor_contratual
    FROM dim_detalhes_contratos
    WHERE chave_contratos != 1
    ORDER BY valor_contratual desc
    LIMIT 5;

CREATE VIEW  view_contratos_menor_valor AS
    SELECT chave_contratos,objeto,valor_contratual
    FROM dim_detalhes_contratos
    WHERE chave_contratos != 1
    ORDER BY valor_contratual 
    LIMIT 5;



CREATE VIEW  view_entidades_mais_contratos_adjudicados AS
    SELECT nome, count(*) AS numero_contratos, adjudicante, sum(valor_contratual) AS valor_adjudicado
    FROM fact_contratos ct
    LEFT JOIN dim_entidade deadjudicante
                    ON deadjudicante.chave_entidade = ct.adjudicante
    GROUP BY adjudicante
    ORDER BY count(*) desc
    LIMIT 5; 



CREATE VIEW  view_entidades_mais_concorrem_menos_ganham AS
    SELECT de.nome,de.chave_entidade,
        COUNT(*) AS total_concursos,
        SUM(
            CASE 
                WHEN ct.adjudicatario = 1 THEN 1
                ELSE 0
            END
        ) AS total_vitorias,
        SUM(
            CASE 
                WHEN ct.adjudicatario = 0 THEN 1
                ELSE 0
            END
        ) AS total_derrotas,
        ROUND(
            SUM(CASE WHEN ct.adjudicatario = 1 THEN 1 ELSE 0 END)
            / COUNT(*) * 100,
            2
        ) AS taxa_vitoria
    FROM fact_contratos ct
    LEFT JOIN dim_entidade de
        ON de.chave_entidade = ct.chave_entidade
    GROUP BY de.chave_entidade, de.nome
    HAVING COUNT(*) >= 5
    ORDER BY taxa_vitoria ASC, total_concursos DESC
    LIMIT 5;

ALTER TABLE cpv_dim
    ADD FULLTEXT ft_cpv_search (codigo, cpv_descricao, descricao);
DELIMITER $$
CREATE PROCEDURE search_cpv(IN input TEXT)
BEGIN
    SELECT
        COUNT(cp.chave_contrato) AS quantidade_contratos,
        SUM(dc.valor_contratual) AS valor_total
    FROM dim_cpv_contratos cp
         LEFT JOIN dim_detalhes_contratos dc
               ON cp.chave_contrato = dc.chave_contratos
         LEFT JOIN cpv_dim c
               ON cp.chave_cpv = c.chave_cpv
    WHERE
        MATCH(c.codigo, c.cpv_descricao, c.descricao)
        AGAINST (CONCAT(input, '*') IN BOOLEAN MODE);
    -- AGAINST (input IN NATURAL LANGUAGE MODE);
END$$
DELIMITER ;
