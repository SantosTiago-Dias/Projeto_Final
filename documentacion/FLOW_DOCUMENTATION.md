# ETL Flow Documentation

## Overview
The ETL (Extract, Transform, Load) pipeline processes contract data and related information, transforming it from source data into a dimensional data warehouse model. The main execution flow is managed by `main.py`.

---

## Complete ETL Flow

### 1. **CONNECTION PHASE** 🔌
**File:** `database_aux.py`
- **Purpose:** Establish connection with the database
- **Method:** `db.get_connection()`
- **Status Codes:**
  - ✅ Success: Continue with extraction
  - ❌ Failure: Exit with error code 1

**What happens:**
- Loads environment variables from `.env` file
- Creates database connection using credentials
- Validates connection is active

---

### 2. **EXTRACTION PHASE** 📥
**Files:** 
- `extracao_incremental_contratos.py` 
- `extracao_incremental_entidades.py` 
- `database_aux.py` → `verify_database_exists()`

**Purpose:** Extract data from source systems/APIs
- **Current Status:** Database verification only (extraction from external sources is commented out)
- **Methods:**
  - `db.verify_database_exists()`: Validates target database structure
  - `extracao_incremental_contratos.main()`: Would extract contracts incrementally
  - `extracao_incremental_entidades.main()`: Available for entity extraction

**What happens:**
- Verifies the data warehouse schema exists
- Prepares environment for transformation

---

### 3. **TRANSFORMATION PHASE** 🔄
**File:** `database_aux.py` → `execute_transformacao()`

**Purpose:** Clean and restructure raw data into dimensional model

- Data is transfrom from `extrac` tables and is saved in:
  - `cpv_contratos_transf` (Classification codes)
  - `contratos_transf` (Contract details)
  - `entidade_transf` (Entities/Organizations)

**What happens:**
- Applies business logic transformations
- Normalizes and structures data into star schema
- Prepare data for to be loaded for final model

---

### 4. **DATA POPULATION PHASE** 📊

Uses ceberas(IA) to help populate data

**Files:** (executed in order)
1. `cpv_synonyms.py` → Load CPV (Classification of Procurement) synonyms
2. `tipoContratos_synonymos.py` → Load contract type synonyms
3. `tipoProcedimento_synonymos.py` → Load procedure type synonyms
4. `justificacaoNEscrita.py` → Load justification data
5. `artigos_synonymos.py` → Load article/regulation synonyms

**Supporting Files:**
- `dictonary_aux.py`: Helper functions for dictionary/lookup management
- `database_aux.py`: Database operations

**Purpose:** Populate reference data and dimension tables
- Load standardized lookups and synonyms
- Enrich main dataset with classification codes
- Ensure referential integrity

**What happens:**
- Inserts standardized reference data into lookup tables
- Creates mappings between original and standardized values
- Validates all data against business rules

---

### 5. **LOAD PHASE** 📤

**File:** `database_aux.py`

**Methods (in order):**
1. `db.ensure_dim_data()`: Validates/creates date dimension
2. `db.execute_load()`: Final load into data warehouse

**Purpose:** Load transformed and enriched data into the dimensional model

**What happens:**
- Ensures all dimension tables are complete (especially date dimension)
- Loads fact table with aggregated contract data
- Updates materialized views (if any)
- Completes the data warehouse population

---

## Error Handling

Each phase has try-catch blocks that:
- Log detailed error messages using loguru
- Exit the process immediately on failure (sys.exit(1))
- Prevent partial data loads from corrupting the warehouse

**Failure Points:**
- 🔌 Database connection fails → Phase 1 exit
- 📥 Extraction verification fails → Phase 2 exit
- 🔄 Transformation fails → Phase 3 exit
- 📊 Data population fails → Phase 4 exit
- 📤 Load fails → Phase 5 exit

---

## Data Flow Diagram

```
[SOURCE DATA]
     ↓
[EXTRACTION] (verify_database_exists)
     ↓
[TRANSFORMATION] (execute_transformacao)
     ↓
[DATA POPULATION] 
  ├→ CPV Synonyms
  ├→ Contract Type Synonyms
  ├→ Procedure Type Synonyms
  ├→ Justifications
  └→ Article Synonyms
     ↓
[LOAD]
  ├→ ensure_dim_data (Date dimension)
  ├→ execute_load (Fact table load)
  └→ Update Data Warehouse
     ↓
[DATA WAREHOUSE] ✅
```

---

## Key Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `main.py` | Orchestrates entire ETL flow | Active |
| `database_aux.py` | Database operations & transformations | Core |
| `cpv_synonyms.py` | Load CPV classifications | Population |
| `tipoContratos_synonymos.py` | Load contract types | Population |
| `tipoProcedimento_synonymos.py` | Load procedure types | Population |
| `justificacaoNEscrita.py` | Load justifications | Population |
| `artigos_synonymos.py` | Load article data | Population |
| `dictonary_aux.py` | Dictionary/lookup helpers | Support |
| `extracao_incremental_contratos.py` | Extract contracts (disabled) | Available |
| `extracao_incremental_entidades.py` | Extract entities | Available |

---

## Execution Time Estimate
- Total pipeline: ~4-5 hours(depending on data volume)
- Longest phase: Typically LOAD (full fact table population)

## Logging
All operations are logged using `loguru` for debugging and monitoring.
Logs help track:
- Successful phase completions
- Error diagnosis
- Performance metrics

---

**Last Updated:** 05 May 2026
