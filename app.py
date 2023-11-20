import multiprocessing
import warnings
warnings.filterwarnings("ignore")
import sys
import logging
import time
import subprocess
from wd import check_stream
from config import *
from service import run
from datetime import datetime, timedelta
import os
import signal
import psutil

if __name__ == '__main__':
  multiprocessing.freeze_support()
  run()
   
