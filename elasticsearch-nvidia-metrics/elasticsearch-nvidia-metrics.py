#!/usr/bin/env python

from elasticsearch import Elasticsearch
import random, time, os
from functools import reduce  # forward compatibility for Python 3
import operator
import subprocess
import csv,json
import StringIO
import datetime
import signal
import datetime

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)
interrupted = False

es = Elasticsearch(os.getenv('ES_HOST_LIST', 'http://elasticsearch.jamiehouse:9200').split(','), 
                   maxsize=os.getenv('ES_MAX_CONNECTIONS', 25))

def get_nvidia_metrics():
  if os.getenv('MOCK', False):
    metrics_str = '0, GPU-9c9290a3-b54e-adb6-02ff-9cf106b50ca3, 44, 65, 3403\n1, GPU-adf23210-605a-ade1-549d-9fc5996f1f9c, 43, 64, 3403\n2, GPU-72ddad7f-26cb-9d2b-8a74-781877b7d575, 47, 68, 3403\n3, GPU-cd6b309d-8885-e7d2-6aae-834381efa24a, 44, 65, 3403\n4, GPU-29b23a6a-d622-9f37-4e18-9ed0cfde2daa, 47, 68, 3403\n5, GPU-ef77ef4a-2670-76ea-4be0-92c90c173a41, 48, 69, 3403\n'
  else:
    metrics_str = subprocess.check_output(["nvidia-smi", "--query-gpu=index,gpu_uuid,fan.speed,temperature.gpu,memory.used", "--format=csv,noheader,nounits"])
  return metrics_str

def send_to_elasticsearch(metrics_str):
  f = StringIO.StringIO(metrics_str)
  reader = csv.DictReader(f, delimiter=',', fieldnames=['index', 'gpu_uuid', 'fanspeed', 'temperaturegpu', 'memoryused'], skipinitialspace=True)
  for row in reader:
    doc = {
      'timestamp': datetime.datetime.now(),
      'index': int(row['index']),
      'gpu_uuid': row['gpu_uuid'],
      'fanspeed': int(row['fanspeed']),
      'temperaturegpu': int(row['temperaturegpu']),
      'memoryused': int(row['memoryused']),
      'node_name': os.getenv('NODE_NAME', os.getenv('HOSTNAME', 'localhost'))
    }

    if os.getenv("DEBUG", False):
      print("doc: %s" % doc)
    retval = es.index(index=os.getenv('ES_INDEX', 'nvidia-metrics') + '-' + datetime.datetime.now().strftime('%Y.%m.%d'),
                      doc_type='nvidia-metrics',
                      body=doc)

if __name__ == '__main__':
  # Generate some requests.
  while not interrupted:
    try:
      metrics_str = get_nvidia_metrics()
      send_to_elasticsearch(metrics_str)
    except ex:
      print("Caught exception: " + ex)
    time.sleep(os.getenv('SLEEP_TIME', 10))

