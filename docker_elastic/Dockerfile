FROM docker.elastic.co/elasticsearch/elasticsearch:8.16.1

ENV discovery.type="single-node"
ENV xpack.security.enabled="false"
ENV logger.level="warn"
ENV m="4GB"

COPY bulk_data.json /usr/share/elasticsearch/bulk_data.json

COPY landmarks_mapping.json /usr/share/elasticsearch/landmarks_mapping.json

COPY articles_snippets_emb_mapping.json /usr/share/elasticsearch/articles_snippets_emb_mapping.json

COPY articles_emb_mapping.json /usr/share/elasticsearch/articles_emb_mapping.json

COPY send_request.sh /usr/share/elasticsearch/send_request.sh

USER root 
RUN chmod +x /usr/share/elasticsearch/send_request.sh
USER elasticsearch

CMD ["/bin/bash", "/usr/share/elasticsearch/send_request.sh"]
