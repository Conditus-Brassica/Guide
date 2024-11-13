# Docker для Elasticsearch

```bash
docker build -t elastic_docker .
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elastic_docker
