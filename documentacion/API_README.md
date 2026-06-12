# DB FAIR API Documentation
## Overview

- Base API paths:
  - `/contracts`
  - `/contracts/{chave_contrato}`
  - `/contracts/numberContracts`
  - `/entidades`
  - `/entidades/{chave_entidade}`
  - `/entidades/{chave_entidade}/listContracts`
  - - `/entidades/numberEntities`
  - `/filters`
  

- Response formats are JSON.
- Pagination is used for list endpoints with 25 items per page.
- Error responses include `422` for invalid search data, `404` for not found, and `500` for server failures.

## Tags

- `Contratos`: Operations related to public contracts.
- `Entidades`: Operations related to contracting entities (adjudicante, adjudicatária, or competitors).
- `Filtros`: Available filter data for contract search.

## Endpoints

### GET `/contracts`

Returns a paginated list of contracts.

#### Query parameters

- `page` (integer): page number.
- `tipo_contrato` (integer): filter by contract type ID.
- `tipo_procedimento` (integer): filter by procedure type ID.
- `data_publicacao_inicio` (string, date): publication start date (`YYYY-MM-DD`).
- `data_publicacao_fim` (string, date): publication end date (`YYYY-MM-DD`).
- `valor_contratual` (number): filter by contract value.
- `prazo_execucao` (integer): filter by execution period in days.
- `contrato_ecologico` (integer): ecological contract flag (`0 = Não`, `1 = Sim`).
- `procedimento_centralizado` (integer): centralized procedure flag (`0 = Não`, `1 = Sim`).
- `cpvs` (string): search by CPV code, description, or synonyms.

#### Success response

- `200`: paginated contract list.
- Response body includes:
  - `data`: array of `ContratoResumo` objects.
  - `links`: pagination links.
  - `meta`: pagination metadata.

### GET `/contracts/{chave_contrato}`

Returns details for a single contract by its unique key.

#### Path parameter

- `chave_contrato` (integer, required): unique contract key.

#### Success response

- `200`: contract details.
- Response body is a `ContratoDetalhe` object.

#### Error responses

- `404`: contract not found.
- `500`: server error.

### GET `/contracts/numberContracts`

Returns number of contracts in database.

#### Success response

- `200`: number of contracts.
- Response body is a `numberContracts` object.

#### Error responses

- `404`: contract not found.
- `500`: server error.

### GET `/entidades`

Returns a paginated list of entities.

#### Query parameters

- `page` (integer): page number.
- `nome` (string): filter by partial entity name.
- `nif` (string): filter by entity NIF.
- `pais` (string): filter by entity country.

#### Success response

- `200`: paginated entity list.
- Response body includes:
  - `data`: array of `Entidade` objects.
  - `links`: pagination links.
  - `meta`: pagination metadata.

### GET `/entidades/{chave_entidade}`

Returns details for a single entity by its unique key.

#### Path parameter

- `chave_entidade` (integer, required): unique entity key.

#### Success response

- `200`: entity details.
- Response body is an `Entidade` object.

#### Error responses

- `404`: entity not found.
- `500`: server error.

### 5. GET `/entidades/{chave_entidade}/listContracts`

Returns a paginated list of contracts associated with a specific entity, either as adjudicante or adjudicatária.

#### Path parameter

- `chave_entidade` (integer, required): unique entity key.

#### Success response

- `200`: paginated contract list for the entity.
- Response body uses the same structure as `/contracts`.

#### Error responses

- `404`: entity not found.
- `500`: server error.

### GET `/entidades/numberEntities`

Returns number of entities in database.

#### Success response

- `200`: number of Entities.
- Response body is a `numberEntities` object.

#### Error responses

- `404`: contract not found.
- `500`: server error.

### 6. GET `/filters`

Returns available filter metadata for contract queries.

#### Success response

- `200`: available filters.
- Response body includes:
  - `TipoContrato`: array of contract type objects.
  - `TipoProcedimento`: array of procedure type objects.

## Schemas

### `ContratoResumo`

A contract summary includes:
- `chave_contratos`: unique contract key.
- `id_contrato`: contract ID.
- `objeto`: contract title or object.
- `descricao`: contract description.
- `data_publicacao`: publication date.
- `valor_contratual`: contract value.
- `contrato_ecologico`: ecological contract flag.
- `prazo_execucao`: execution period.
- `procedimento_centralizado`: centralized procedure flag.
- `cpvs`: array of CPV references.
- `adjudicante`: entity reference.
- `tipo_contrato`: contract type reference.
- `tipo_procedimento`: procedure type reference.
- `data`: date info reference.
- `concorrentes`: list of competitors.

### `ContratoDetalhe`

Extends `ContratoResumo` with:
- `data_celebracao`: contract signing date.
- `local_execucao`: execution location.
- `num_acordos_quadro`: framework agreement number.
- `desc_acordo_quadro`: framework agreement description.
- `data_fecho_contrato`: contract closing date.
- `valor_total_efetivo`: effective total value.
- `regime`: legal regime.
- `tipo_fim_contrato`: end-of-contract type.
- `crit_materiais`: material criteria flag.
- `link_pecas`: link to contract documents.
- `observacoes`: observations.
- `fundamentacao_ajuste_directo`: direct award justification.

### `CPV`

Represents a CPV classification:
- `id_cpv`
- `codigo`
- `cpv_descricao`
- `descricao`

### `Entidade`

Represents an entity:
- `id_entidade`
- `nif`
- `nome`
- `num_contratos_adjudicatario`
- `num_contratos_adjudicante`
- `pais`

### `TipoContrato`

Contract type object:
- `id`
- `tipo`
- `descricao`

### `TipoProcedimento`

Procedure type object:
- `id`
- `tipo`
- `descricao`

### `DataInfo`

Date metadata object:
- `date`
- `feriado`
- `fim_semana`
- `data_extenso`
- `evento_natural`

### `Concorrente`

Competitive participant object:
- `entidade`: entity reference.
- `adjudicatario`: flag indicating whether the entity is the adjudicatário.

### Pagination

Common pagination responses include:
- `links`: first, last, prev, next URLs.
- `meta`: current page, total pages, items per page, and link objects.

## Usage notes

- Use `/filters` first to retrieve valid `tipo_contrato` and `tipo_procedimento` values.
- Search filters are optional and can be combined.
- Use entity or contract ID paths to fetch detailed records.
- Paginated endpoints return consistent `data`, `links`, and `meta` shapes.

## Example

Fetch the first page of contracts:

```http
GET /contracts?page=1
```

Fetch contract details:

```http
GET /contracts/2
```

Fetch entity contracts:

```http
GET /entidades/246088/listContracts
```
