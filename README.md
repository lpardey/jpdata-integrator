# JPData Integrator

This project extracts, organizes, and stores judicial process information from [Consulta de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros) website using a robust and efficient pipeline. It is designed with scalability and performance in mind, making it a reliable solution for processing and exposing large volumes of judicial data.


## Key features:

- **Asynchronous Data Extraction:**  
  Parallel data extraction supported by `asyncio` and `aiohttp` to maximize throughput and performance. This approach ensures that the scraping process is both fast and efficient.

- **Data Modeling and Validation:**  
  The extracted data is modeled using `Tortoise ORM` and validated with `Pydantic`, ensuring robust and accurate data handling.

- **Database Management:**  
  Data is stored in a `PostgreSQL` database, providing a scalable and reliable storage solution. The use of `Tortoise ORM` simplifies database interactions and ensures that data relationships are well-managed.

- **REST API Implementation:**  
  `FastAPI` is used to expose the data through secure and efficient endpoints.

- **Automated Testing:**  
  `Pytest` is employed for automated testing, ensuring the code’s scalability, robustness, and maintainability.

- **Containerized Deployment:**  
  `Docker` is used to containerize the application, facilitating seamless deployment and execution across different environments.


## Benchmark Tests 

### Test Parallel Extraction (Litigantes)

```
pytest --log-cli-level INFO tests/test_crawler_e2e.py::test_crawler_parallel_litigantes


tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[1] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 17230202414350: 1/11
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 9, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 51.0444016456604
PASSED   [ 20%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[2]  
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 9, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 32.785863637924194
PASSED   [ 40%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[5] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 9, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 14.386630535125732
PASSED   [ 60%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[10] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 17203201600358G: 1/2
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 9, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 9.640607833862305
PASSED   [ 80%]

tests/test_crawler_e2e.py::test_crawler_parallel_litigantes[15] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_litigantes.time.start
INFO     root:concurrency.py:9 Task Litigante  - Causa 08256202400340: 1/1
...
INFO     root:test_crawler_e2e.py:40 Results: [11, 1, 8, 9, 1, 11, 1, 5, 8, 2, 1, 4, 1, 1, 3]
INFO     root:time_decorator.py:16 run_multiple_litigantes.time.end: 7.0401105880737305
PASSED   [100%]
```

#### Results:

| Test | Time | Tasks |
|------|------|-------|
| test_crawler_parallel_litigantes | 51.0444016456604  | 1  |
| test_crawler_parallel_litigantes | 32.785863637924194 | 2  |
| test_crawler_parallel_litigantes | 14.386630535125732 | 5  |
| test_crawler_parallel_litigantes | 9.640607833862305 | 10 |
| test_crawler_parallel_litigantes | 7.0401105880737305 | 15 |


### Test Parallel Extraction (Causas)
```
pytest --log-cli-level INFO tests/test_crawler_e2e.py::test_crawler_parallel_causas

tests/test_crawler_e2e.py::test_crawler_parallel_causas[1] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/143
...

INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 0930420060269: 143/143
INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 67.81063055992126
PASSED   [ 33%]

tests/test_crawler_e2e.py::test_crawler_parallel_causas[5] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/143
...

INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 12.668936967849731
PASSED   [ 66%]

tests/test_crawler_e2e.py::test_crawler_parallel_causas[15] 
------------------------------------------------------------------------ live log call ------------------------------------------------------------------------
INFO     root:time_decorator.py:13 run_multiple_causas.time.start
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 13284202419612: 1/143
...
INFO     root:concurrency.py:9 Task Litigante 0968599020001 - Causa 0930420060269: 143/143
INFO     root:time_decorator.py:16 run_multiple_causas.time.end: 7.249382495880127
PASSED   [100%]
```

#### Results:

| Test | Time | Tasks |
|------|------|-------|
| test_crawler_parallel_causas | 67.81063055992126  | 1  |
| test_crawler_parallel_causas | 12.668936967849731 | 5  |
| test_crawler_parallel_causas | 7.249382495880127 | 15 |
