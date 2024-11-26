# Docker для Elasticsearch

```bash
docker build -t elastic_docker .
docker run --name "Elastic_Container" -d -p 9200:9200 -m "4GB" -e "discovery.type=single-node" -e "xpack.security.enabled=false" elastic_docker
```
