FROM python:2-alpine

COPY dist /dist

RUN pip install /dist/elasticsearch-nvidia-metrics*.tar.gz

CMD ["/usr/local/bin/python", \
     "-u", \
     "/usr/local/bin/elasticsearch-nvidia-metrics.py"]
