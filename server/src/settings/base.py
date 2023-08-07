import datetime
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

SERVER_HOST = os.environ['SERVER_HOST']
SERVER_PORT = int(os.environ['SERVER_PORT'])

STATUS_TIMEOUT = int(os.environ['STATUS_TIMEOUT'])

QUEUE_MAX_SIZE = int(os.environ['QUEUE_MAX_SIZE'])

MIN_DURATION = datetime.time(0, 0, int(os.environ['MIN_DURATION']))
MAX_DURATION = datetime.time(0, int(os.environ['MAX_DURATION']), 0)

time_duration_max = datetime.time(0, 30, 0)
time_duration_min = datetime.time(0, 0, 5)

