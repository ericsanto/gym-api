# Etapa de build
FROM python:3.12-alpine AS builder

WORKDIR /app

# Instala dependências necessárias para compilar bibliotecas
RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq

# Copia as dependências do projeto
COPY requirements.txt requirements.txt
# Instala as dependências do Python no diretório temporário
RUN pip install --prefix=/install -r requirements.txt

# Etapa final
FROM python:3.12-alpine

# Instala apenas as dependências de runtime (libpq)
RUN apk add --no-cache libpq

WORKDIR /app

# Copia as dependências instaladas no estágio de build
COPY --from=builder /install /usr/local

# Copia o código do projeto
COPY . /app
RUN chmod +x entrypoint.sh