#!/bin/bash
/usr/local/bin/docker-entrypoint.sh &
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|yellow'; do
 sleep 5
done

curl http://localhost:9200/landmarks_index -XPUT -H "Content-Type: application/json" -d @/usr/share/elasticsearch/landmarks_mapping.json 

curl http://localhost:9200/articles_snippets_emb -XPUT -H "Content-Type: application/json" -d @/usr/share/elasticsearch/articles_snippets_emb_mapping.json 

curl http://localhost:9200/articles_emb -XPUT -H "Content-Type: application/json" -d @/usr/share/elasticsearch/articles_emb_mapping.json 

curl http://localhost:9200/landmarks_index/_bulk -XPOST -H 'Content-Type: application/json' --data-binary @/usr/share/elasticsearch/bulk_data.json 

wait 
