# Prueba Tusdatos.co

Proyecto de web scraping de [Consulta de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros).  
Este proyecto extrae y almacena información estructurada sobre procesos judiciales en una base de datos, expuesta a través de una API implementada con FastAPI. Utiliza Pytest para pruebas automatizadas y Docker para facilitar el despliegue y la ejecución.


## Tecnologías [^1]

- Python: 3.12
- Docker: 26.1.3
- FastAPI: 0.111.0 
- SQLite: 3.40.1
- Tortoise ORM: 0.21.3
- Pytest: 8.2.2


## Test Paralelizando Litigantes

```
pytest --log-cli-level INFO tests/test_crawler_e2e.py::test_crawler_parallel_litigantes


tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[1] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 17230202414350: 1/11
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 8, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 55.76549196243286
PASSED   [ 20%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[2]  
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 8, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 26.918065309524536
PASSED   [ 40%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[5] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 8, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 12.14177680015564
PASSED   [ 60%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[10] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 17203201600358G: 1/2
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 8, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 6.164646148681641
PASSED   [ 80%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[15] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 8, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 5.627331495285034
PASSED   [100%]
```

### Resultados:

| Test | Time | Tasks |
|------|------|-------|
| test_crawler_parallel_litigantes | 55.76549196243286  | 1  |
| test_crawler_parallel_litigantes | 26.918065309524536 | 2  |
| test_crawler_parallel_litigantes | 12.14177680015564 | 5  |
| test_crawler_parallel_litigantes | 6.164646148681641 | 10 |
| test_crawler_parallel_litigantes | 5.627331495285034 | 15 |


## Test Paralelizando Causas
```
pytest --log-cli-level INFO tests/test_crawler_e2e.py::test_crawler_parallel_causas

tests/test_crawler_e2e.py::test_crawler_parallel_causas[1] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/144
...

INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 0930420060269: 144/144
INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 67.81063055992126
PASSED   [ 33%]

tests/test_crawler_e2e.py::test_crawler_parallel_causas[5] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/144
...

INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 12.668936967849731
PASSED   [ 66%]

tests/test_crawler_e2e.py::test_crawler_parallel_causas[15] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/144
...
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 0930420060269: 144/144
INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 7.249382495880127
PASSED   [100%]
```

### Resultados:

| Test | Time | Tasks |
|------|------|-------|
| test_crawler_parallel_causas | 67.81063055992126  | 1  |
| test_crawler_parallel_causas | 12.668936967849731 | 5  |
| test_crawler_parallel_causas | 7.249382495880127 | 15 |


[^1]: Para obtener una lista completa de tecnologías y dependencias, ver requirements.txt y requirements-dev.txt.