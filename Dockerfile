FROM python:3.12 AS base

WORKDIR /jpdata_integrator
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM base AS dev

COPY requirements-dev.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -r requirements-dev.txt

FROM base AS prod

COPY . .
CMD ["uvicorn", "consulta_pj.app:app", "--host", "0.0.0.0", "--port", "8000"]
