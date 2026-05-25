# Database Overview

This README explains the database structure used by the project, based on `init.sql` and `procedures.sql`.

## Purpose

The database is designed to support an ETL pipeline for public contract data. It includes:

- logs tables (`*_logs`)
- raw extraction tables (`*_ext`)
- transformation staging tables (`*_transf`)
- populated data tables (`*_dictonary`)
- dimensional model tables (`dim_*` and `fact_contratos`)
- dictionaries for consistent reference values
- logging tables for ETL status tracking

## Table Types

Each table belongs to one of these functional categories:

- `Logging tables`: track ETL steps and statuses.
- `Dictionary tables`: store normalized reference values and labels.
- `Raw extraction tables`: hold imported data before transformation.
- `Transformation staging tables`: store cleaned and normalized intermediate data.
- `Dimensional tables`: define the final analytical schema.
- `Fact tables`: record relationships and numerical measures for analytics.
- `Lookup tables`: support normalization through reusable mappings.

## Files

- `init.sql`: creates tables, constraints, dictionaries, and initial lookup values.
- `procedures.sql`: defines SQL functions and stored procedures to transform and load data.

## Key Table Groups

### Logging

- `t_logs_extract`: logs extraction operations.
- `t_logs_transformacao`: logs transformation operations.
- `t_logs_carregamento`: logs loading operations.

Each log table stores status values: `INICIO`, `SUCESSO`, or `ERRO`.

### Reference Dictionaries

- `cpv_dictionary`
- `tipo_procedimento_dictionary`
- `tipo_contrato_dictionary`
- `justificacao_contrato_nao_escrito_dictionary`
- `fundamentacao_contrato_dictionary`

These tables store normalized reference values for CPV codes, contract types, procedure types, justifications, and legal foundations.

### Raw/Staging Tables

- `entidades_ext`: raw entity records from extraction.
- `contratos_ext`: raw contract records from extraction.

These tables keep the extracted data in its original form before transformation.

### Transformation Tables

- `entidade_transf`: transformed entity data with metrics and normalized names.
- `detalhes_contratos_transf`: transformed contract details with typed dates and numeric values.
- `contratos_transf`: transformed contract-to-entity relationships, including adjudicante and concorrentes.
- `cpv_contratos_transf`: normalized CPV code relationships for contracts.

### Dimensional Model Tables

- `dim_entidade`: dimension table for entities.
- `dim_detalhes_contratos`: dimension table for contract details.
- `dim_cpv_contratos`: bridge table linking contracts to CPV entries.
- `dim_data`: date dimension table with holiday and weekday metadata.
- `fact_contratos`: fact table linking contract, entity, type, procedure, and date dimensions.

This structure supports reporting and analytics via a star schema.

### Lookup Tables

- `lookup_abreviaturas`: stores abbreviation replacements for normalization.

## Table Definitions

### `data_extracted`
- `id`: auto-increment PK.
- `num_contratos`: number of contracts extracted.
- `media_contratos`: average contract value.
- `data_extracao`: extraction timestamp.

### `t_logs_extract`
- `id`: auto-increment PK.
- `nome_objeto`: object name being extracted.
- `status`: `INICIO`, `SUCESSO`, or `ERRO`.
- `mensagem`: log message.
- `ultima_extracao`: last update timestamp.

### `t_logs_transformacao`
- same as `t_logs_extract`, for transformation steps.

### `t_logs_carregamento`
- same as `t_logs_extract`, for loading steps.

### `cpv_dictionary`
- `id_cpv`: auto-increment PK.
- `codigo`: CPV code string.
- `cpv_descricao`: CPV short description.
- `descricao`: extended CPV description.

### `tipo_procedimento_dictionary`
- `id_tipo_procedimento`: auto-increment PK.
- `tipo`: procedure type name.
- `descricao`: description of the procedure type.

### `tipo_contrato_dictionary`
- `id_tipo_contrato`: auto-increment PK.
- `tipo`: contract type name.
- `descricao`: description of the contract type.

### `justificacao_contrato_nao_escrito_dictionary`
- `id_justificacao`: auto-increment PK.
- `justificacao`: justification text.
- `descricao`: explanation of the justification.

### `fundamentacao_contrato_dictionary`
- `id_fundamentacao`: auto-increment PK.
- `fundamentacao`: legal foundation text.
- `descricao`: explanation of the legal foundation.

### `entidades_ext`
- `id_entidade`: entity ID from raw data.
- `nif`: entity tax number.
- `nome`: entity name.
- `pais`: entity country.

### `contratos_ext`
- `id_contrato`: raw contract ID.
- `tipo_contrato`: raw contract type text.
- `tipo_procedimento`: raw procedure type text.
- `objeto`: contract object/title.
- `descricao`: contract description.
- `adjudicante`: JSON text with adjudicating entity data.
- `data_publicacao`: raw publication date string.
- `data_celebracao`: raw celebration date string.
- `valor_contratual`: raw contract value string.
- `cpvs`: raw CPV codes string.
- `cpvsDesignation`: raw CPV descriptions string.
- `prazo_execucao`: raw execution deadline string.
- `local_execucao`: raw execution location.
- `fundamentacao`: raw legal foundation text.
- `procedimento_centralizado`: centralized procedure flag string.
- `num_acordos_quadro`: raw framework agreement count.
- `desc_acordo_quadro`: framework agreement description.
- `data_fecho_contrato`: raw closing date string.
- `valor_total_efetivo`: raw effective total value string.
- `regime`: legal regime text.
- `justificacao_nao_escrita`: raw non-written justification text.
- `tipo_fim_contrato`: contract end type.
- `crit_materiais`: materials criteria flag string.
- `concorrentes`: JSON text with competitor entities.
- `adjudicatarios`: JSON text with awarded entities.
- `link_pecas`: URL for contract documents.
- `observacoes`: observations.
- `contrato_ecologico`: ecological contract flag string.
- `fundamentacao_ajuste_directo`: direct award justification.

### `entidade_transf`
- `id_entidade`: entity ID.
- `nif`: normalized tax number.
- `nome`: normalized entity name.
- `total_adjudicatario`: sum of contract values where entity is adjudicatário.
- `num_contratos_adjudicatario`: number of contracts as adjudicatário.
- `total_adjudicante`: sum of contract values where entity is adjudicante.
- `num_contratos_adjudicante`: number of contracts as adjudicante.
- `pais`: country.
- `distrito`: district.

### `detalhes_contratos_transf`
- `id_contrato`: contract ID.
- `objeto`: normalized contract object/title.
- `descricao`: normalized description.
- `data_publicacao`: normalized publication date.
- `data_celebracao`: normalized celebration date.
- `valor_contratual`: normalized numeric contract value.
- `prazo_execucao`: execution period in days.
- `local_execucao`: normalized execution location.
- `procedimento_centralizado`: binary centralized procedure flag.
- `num_acordos_quadro`: framework agreement count.
- `desc_acordo_quadro`: framework agreement description.
- `data_fecho_contrato`: normalized closing date.
- `valor_total_efetivo`: normalized effective total value.
- `regime`: legal regime.
- `tipo_fim_contrato`: contract end type.
- `crit_materiais`: binary materials criteria flag.
- `link_pecas`: URL for documents.
- `observacoes`: normalized observations.
- `contrato_ecologico`: binary ecological contract flag.
- `fundamentacao_ajuste_directo`: direct award justification.

### `contratos_transf`
- `id_contrato`: contract ID.
- `id_adjudicante`: adjudicating entity ID.
- `id_entidade`: related entity ID (adjudicatário or competitor).
- `adjudicatario`: flag `1` if entity is awarded party, `0` otherwise.
- `tipo_contrato`: normalized contract type.
- `tipo_procedimento`: normalized procedure type.
- `fundamentacao`: legal foundation.
- `justificacao_nao_escrita`: non-written justification.

### `cpv_contratos_transf`
- `id_contrato`: contract ID.
- `cpv`: raw CPV code.
- `cpv_descricao`: raw CPV description.

### `dim_entidade`
- `chave_entidade`: surrogate key.
- `id_entidade`: original entity ID.
- `nif`: tax number.
- `nome`: entity name.
- `total_adjudicatario`: awarded contract total.
- `num_contratos_adjudicatario`: awarded contract count.
- `total_adjudicante`: contracting contract total.
- `num_contratos_adjudicante`: contracting contract count.
- `pais`: country.
- `distrito`: district.

### `dim_detalhes_contratos`
- `chave_contratos`: surrogate contract key.
- `id_contrato`: original contract ID.
- `objeto`: contract title.
- `descricao`: contract description.
- `data_publicacao`: publication date.
- `data_celebracao`: signing date.
- `valor_contratual`: contract value.
- `prazo_execucao`: execution period in days.
- `local_execucao`: execution location.
- `procedimento_centralizado`: binary centralized procedure flag.
- `num_acordos_quadro`: framework agreement count.
- `desc_acordo_quadro`: framework agreement description.
- `data_fecho_contrato`: closing date.
- `valor_total_efetivo`: effective total value.
- `regime`: legal regime.
- `tipo_fim_contrato`: contract end type.
- `crit_materiais`: binary materials criteria flag.
- `link_pecas`: document link.
- `observacoes`: observations.
- `contrato_ecologico`: binary ecological contract flag.
- `fundamentacao_ajuste_directo`: direct award justification.

### `dim_cpv_contratos`
- `chave_contrato`: contract surrogate key.
- `chave_cpv`: CPV dictionary key.

### `dim_data`
- `chave_date`: surrogate date key.
- `data`: actual date.
- `feriado`: holiday name or `Não aplicável.`.
- `fim_semana`: weekend flag.
- `dia`: day of month.
- `mes`: month number.
- `ano`: year.
- `dia_semana`: weekday name.
- `nome_mes`: month name.
- `abr_mes`: month abbreviation.
- `data_extenso`: human-readable date text.
- `evento_natural`: natural event description.

### `fact_contratos`
- `chave_contratos`: link to `dim_detalhes_contratos`.
- `adjudicante`: adjudicating entity key from `dim_entidade`.
- `chave_entidade`: related entity key from `dim_entidade`.
- `adjudicatario`: binary flag if related entity is adjudicatário.
- `chave_tipo_contrato`: contract type dictionary key.
- `chave_tipo_procedimento`: procedure type dictionary key.
- `chave_fundamentacao`: legal foundation dictionary key.
- `chave_justificacao_nao_escrita`: justification dictionary key.
- `valor_contratual`: contract value.
- `chave_data`: date key from `dim_data`.

## Important Seed Data

The `init.sql` script inserts placeholder records for invalid or unknown values, such as:

- invalid entity record
- invalid contract record
- invalid date record
- `N/A` entries in dictionaries

This allows the ETL process to load incomplete or missing data without failing.

## Procedures and Functions

### Helper Functions

- `normalizar(input TEXT)`: removes HTML line breaks, trims whitespace, and returns normalized text.
- `normalizar_sc(input TEXT)`: normalizes Portuguese abbreviations such as `C/` to `COM` and `S/` to `SEM`.

### Transformation Procedures

- `transform_detalhes_contratos()`: converts raw `contratos_ext` values into typed contract detail rows.
- `transform_contratos()`: builds `contratos_transf` rows for adjudicatários and concorrentes, linking contracts to entity IDs.
- `transform_entidades()`: creates transformed entity rows and computes adjudicatário/adjudicante metrics.
- `transform_cpv_contratos()`: extracts CPV codes and descriptions from `contratos_ext` into `cpv_contratos_transf`.
- `normalizar_lookup(p_table, p_column)`: applies abbreviation replacements using `lookup_abreviaturas`.

### Load Procedures

- `load_dim_entidade()`: loads transformed entity data into `dim_entidade`.
- `load_dim_detalhes_contratos()`: loads transformed contract details into `dim_detalhes_contratos`.
- `load_dim_cpv_contratos()`: populates `dim_cpv_contratos` by matching transformed CPV contracts to dictionary entries.
- `load_dim_data(IN data_inicio DATE, IN data_fim DATE)`: generates date dimension rows across a date range, including Portuguese holidays and weekend flags.
- `load_fact()`: builds the `fact_contratos` fact table with foreign key references into dimensions.

## ETL Flow

A recommended execution order is:

1. Run `init.sql` to create tables and seed lookup data.
2. Run `procedures.sql` to create the helper functions and stored procedures.
3. Execute transformation procedures:
   - `CALL transform_detalhes_contratos();`
   - `CALL transform_contratos();`
   - `CALL transform_entidades();`
   - `CALL transform_cpv_contratos();`
4. Execute load procedures:
   - `CALL load_dim_entidade();`
   - `CALL load_dim_detalhes_contratos();`
   - `CALL load_dim_cpv_contratos();`
   - `CALL load_dim_data('2026-01-01', '2026-12-31');` (adjust date range as needed)
   - `CALL load_fact();`

## Design Notes

- The database follows a layered ETL model: raw extraction (`*_ext`), transformation (`*_transf`), populated data (`*_dictonary`) and final dimensional schema (`dim_*`, `fact_contratos`).
- Text normalization and lookup replacement ensure consistent values across contract records.
- Date normalization and holiday detection are handled in the `dim_data` load procedure.
- Fact table uses surrogate keys and foreign keys for robust analysis and reporting.

## Usage Tips

- Use the dictionary tables to understand allowable values for contract types, procedures, and CPV codes.
- The `dim_data` table supports analytics by date, holiday, weekday, and text-formatted date values.
- Placeholder records such as `N/A` and invalid dimensions prevent referential integrity issues during loading.
