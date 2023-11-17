import warnings
warnings.filterwarnings("ignore")
import sys
import logging
import time
import subprocess
from config import *
from service import run
from datetime import datetime, timedelta
import os
import signal

if __name__ == '__main__':
  run()
   
