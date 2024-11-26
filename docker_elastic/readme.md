# Docker для Elasticsearch

## Установка
```bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.16.1
```
Если не пуллится image, использовать vpn.

## Запуск
```bash
docker build -t elastic_docker .
docker run -p 9200:9200 elastic_docker
