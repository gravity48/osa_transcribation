import binascii
from datetime import datetime


def generate_hash():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time_hash = binascii.crc32(date_time.encode('utf8'))
    date_time_hash = hex(date_time_hash)
    return str(date_time_hash)
