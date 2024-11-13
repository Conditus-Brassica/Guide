FROM elasticsearch:8.15.3 

COPY bulk_data.json /usr/share/elasticsearch/bulk_data.json

COPY landmarks_mapping.json /usr/share/elasticsearch/landmarks_mapping.json

COPY send_request.sh /usr/share/elasticsearch/send_request.sh

USER root 
RUN chmod +x /usr/share/elasticsearch/send_request.sh
USER elasticsearch

CMD ["/bin/bash", "/usr/share/elasticsearch/send_request.sh"]
