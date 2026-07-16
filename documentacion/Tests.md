# Tests

## Structure

```
tests/
└── Feature/
    ├── AnalyticsTest.php
    ├── ContractsTest.php
    └── EntidadesTest.php
```

## Overview

| Test File           | Description                            |
|---------------------|----------------------------------------|
| `AnalyticsTest.php` | Feature tests for the Analytics module |
| `ContractsTest.php` | Feature tests for the Contracts module |
| `EntidadesTest.php` | Feature tests for the Entities module  |

## Running the tests

```bash
docker compose exec api php artisan test
```

*Update this file as new test cases are added or modified.*