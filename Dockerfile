FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword

COPY . /docker-entrypoint-initdb.d

EXPOSE 5432