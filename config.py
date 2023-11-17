# distutils: language = c++
import yaml
from yaml.loader import SafeLoader

headers = { "content-type" : "application/json; charset=utf-8" }

with open('./config.yaml', encoding = 'utf-8') as f:
  config = yaml.load(f, Loader = SafeLoader)


STREAMS = config['streams']
SRS_IP = config['srs_ip']
SRS_PORT = config['srs_port']
RESTART_INTERVAL = config['restart_interval']

# print(STREAMS)