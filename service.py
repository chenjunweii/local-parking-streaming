from config import *
# from wd import check_stream
import wd
import subprocess
import time
import logging
from datetime import datetime, timedelta
import os
import signal
import multiprocessing
from multiprocessing import Pool
import signal
import psutil

logger = logging.getLogger('service.log')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./logs/service.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
  logger.addHandler(handler)


ws = dict() # watch dogs
callbacks = dict()
ps = dict()

def kill_proc_tree(pid, including_parent = True):    
  parent = psutil.Process(pid)
  children = parent.children(recursive = True)
  for child in children:
      child.kill()
  gone, still_alive = psutil.wait_procs(children, timeout = 5)
  if including_parent:
    parent.kill()
    parent.wait(5)


def check_stream_callback (process_name, process_id):
  print('[{}] check_stream_callback / Del Watchdog / Del Stream Process PID [{}]'.format(process_name, process_id))
  kill_proc_tree(process_id, False)
  # os.kill(process_id, signal.SIGINT)
  # ps[process_name].kill()
  # os.kill(os.getpgid(process_id), signal.SIGTERM)
  del ws[process_name]
  del ps[process_name]


def run(): 
  # start_time = datetime.now()
  # multiprocessing.freeze_support()
  pool = Pool(len(STREAMS))

  while True:
    for i, s in enumerate(STREAMS):
      if s['target_url'] not in ps:
        dir = os.getcwd()
        log_filename = os.path.join(dir, 'logs', 'ffmpeg-{}.log'.format(s['target_url']))
        # try:
        #   if os.path.isfile(log_filename):
        #     os.remove(log_filename)
        # except Exception as e:
        #   print('[{}] Remove old log file failed {}'.format(s['target_url'], e))
        c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -stream_loop -1 -re -rtsp_transport tcp -i {}://{}:{}/{} -c:v copy -an -f flv rtmp://{}/live/{} 2> "{}"
        """.format(s['src_protocol'], s['src_ip'], s['src_port'], s['src_url'], SRS_IP, s['target_url'], log_filename)
        # c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -use_wallclock_as_timestamps 1 -stream_loop -1 -re -rtsp_transport tcp -i {}://{}:{}/{} -c:v copy -an -f flv rtmp://{}/live/{}
        # """.format(s['src_protocol'], s['src_ip'], s['src_port'], s['src_url'], SRS_IP, s['target_url'])
        # c = """ffmpeg -fflags +genpts -fflags nobuffer -flags low_delay -strict experimental -use_wallclock_as_timestamps 1 -stream_loop -1 -re -rtsp_transport tcp -i rtsp://127.0.0.1:8554/live.stream-2 -c:v copy -an -f flv rtmp://{}/live/{}
        # """.format(SRS_IP, s['target_url'])
        # print('{} => {}'.format(i, s))
        # ps[s['target_url']] = subprocess.Popen(c, shell = True, text= True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,  close_fds = True)
        ps[s['target_url']] = subprocess.Popen(c, shell = True, text= True, close_fds = True)

        print('[{}] Stream Process {} is created'.format(s['target_url'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        # print(c)
        # logger.debug("Process {} is created".format(s['target_url']))

        def callback (result):
          # print('callback result => ', result) 
          check_stream_callback(s['target_url'], ps[s['target_url']].pid)

        callbacks[s['target_url']] = callback

        if s['target_url'] not in ws:
          # print('[{}] Watchdog is creating'.format(s['target_url']))
          ws[s['target_url']] = pool.apply_async(wd.check_stream, (s['target_url'], ps[s['target_url']].pid, log_filename), callback = callbacks[s['target_url']])
          # ws[s['target_url']] = pool.apply_async(check_stream, (s['target_url'], os.getpgid(ps[s['target_url']].pid), log_filename))
          print('[{}] Watchdog is created'.format(s['target_url']))

    for k, v in ps.copy().items():
      try:
        o = v.poll()
        if o is None:
          pass
          # print('[{}] Stream Process is still alive {}'.format(k, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
          # logger.debug("Process {} is still alive".format(k))
          # if datetime.now() - start_time > timedelta(minutes = RESTART_INTERVAL):
          #   # os.kill(os.getpgid(v.pid), signal.SIGTERM) 
          #   os.kill(v.pid, signal.SIGTERM) 
          #   del ps[k]
          #   time.sleep(1)
          # else:
          # time.sleep(60)
        else:
          print('[{}] Stream Process is dead {}'.format(k, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
          # logger.debug("Process {} is dead".format(k))
          del ps[k]
          time.sleep(1)
      except Exception as e:
        print('[Error] => {}'.format(e))
    time.sleep(5)



if __name__ == '__main__':
  multiprocessing.freeze_support()