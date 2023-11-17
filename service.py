import subprocess
from config import *
import time
import logging
from datetime import datetime, timedelta
import os
import signal

ps = dict()

logger = logging.getLogger('service.log')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./logs/service.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
  logger.addHandler(handler)



def run(): 
  start_time = datetime.now()
  while True:
    for i, s in enumerate(STREAMS):
      if s['target_url'] not in ps:
        c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -stream_loop -1 -re -rtsp_transport tcp -i {}://{}:{}/{} -c:v copy -an -f flv rtmp://{}/live/{}
        """.format(s['src_protocol'], s['src_ip'], s['src_port'], s['src_url'], SRS_IP, s['target_url'])
        
        # c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -use_wallclock_as_timestamps 1 -stream_loop -1 -re -rtsp_transport tcp -i {}://{}:{}/{} -c:v copy -an -f flv rtmp://{}/live/{}
        # """.format(s['src_protocol'], s['src_ip'], s['src_port'], s['src_url'], SRS_IP, s['target_url'])
        # c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -use_wallclock_as_timestamps 1 -stream_loop -1 -re -rtsp_transport tcp -i rtsp://127.0.0.1:8554/live.stream-2 -c:v copy -an -f flv rtmp://{}/live/{}
        # """.format(SRS_IP, s['target_url'])
        # print('{} => {}'.format(i, s))
        # ps[s['target_url']] = subprocess.Popen(c, shell = True, text= True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,  close_fds = True)
        ps[s['target_url']] = subprocess.Popen(c, shell = True, text= True, close_fds = True)

        print('{} Process {} is created'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s['target_url']))
        print(c)

        logger.debug("Process {} is created".format(s['target_url']))

    for k, v in ps.items():
      try:
        o = v.poll()
        if o is None:
          print('{} Process {} is still alive'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), k))
          logger.debug("Process {} is still alive".format(k))

          # if datetime.now() - start_time > timedelta(minutes = RESTART_INTERVAL):
          #   # os.kill(os.getpgid(v.pid), signal.SIGTERM) 
          #   os.kill(v.pid, signal.SIGTERM) 
          #   del ps[k]
          #   time.sleep(1)
          # else:
          time.sleep(60)
        else:
          print('{} Process {} is dead'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), k))
          logger.debug("Process {} is dead".format(k))
          del ps[k]
          time.sleep(1)
      except Exception as e:
        print('[Error] => {}'.format(e))
        time.sleep(1)