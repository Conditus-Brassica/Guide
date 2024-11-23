#!/bin/bash
/usr/local/bin/docker-entrypoint.sh & until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|yellow'; do
	sleep 5
done

curl -X PUT -H "Content-Type: application/json" -d @/usr/share/elasticsearch/landmarks_mapping.json http://localhost:9200/landmarks_index

curl -H 'Content-Type: application/json' -XPOST --data-binary @/usr/share/elasticsearch/bulk_data.json http://localhost:9200/landmarks_index/_bulk

wait
