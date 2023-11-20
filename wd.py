import multiprocessing
import subprocess
import time
from datetime import datetime
import signal
import re
import os


def check_stream(process_name, process_id, log_filename):
  # try:
  #   if os.path.isfile(log_filename):
  #     os.remove(log_filename)
  # except Exception as e:
  #   print('[{}] Remove old log file failed {}'.format(process_name, e))
  while True:
    try:
      print('[{}] Watchdog check_stream'.format(process_name))
      # print('wd : => ', os.getcwd())
      # Read the last line of the ffmpeg.log file
      with open(log_filename, 'r') as log_file:
        log_lines = log_file.readlines()
        if log_lines:
          last_line = log_lines[-1]
        else:
          last_line = ""
      # Extract the frame information using regex
      # print('last line => ', last_line)
      # frame_match = re.search(r'frame=(\d+)fps', last_line, re.IGNORECASE)
      # print('frame_match => ', frame_match)
      # frameA = frame_match.group(1) if frame_match else None
      frameA = last_line
      print('[{}] frameA => {}'.format(process_name, frameA.replace("\n", "")))
      time.sleep(10)
      # Read the last line of the ffmpeg.log file again
      with open(log_filename, 'r') as log_file:
        log_lines = log_file.readlines()
        if log_lines:
            last_line = log_lines[-1]
        else:
            last_line = ""
      # Extract the frame information again
      # frame_match = re.search(r'frame=(\d+)fps', last_line)
      frameB = last_line#frame_match.group(1) if frame_match else None
      print('[{}] frameB => {}'.format(process_name, frameB.replace("\n", "")))
      if frameA == frameB:
          print("[{}] Stream has hung {}".format(process_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
          print('[{}] killing Stream process_id {}'.format(process_name, process_id))
          return
      else:
          print("[{}] Stream looks ok. {}".format(process_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

      time.sleep(2)
    except Exception as e:
      print(e)
    time.sleep(5)

if __name__ == '__main__':
  multiprocessing.freeze_support()