import csv
import sys
import os
import redis
import requests
import datetime

from zipfile import ZipFile
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

TODAY = datetime.datetime.today()
PATH_TO_CSV = os.getenv('PATH_TO_CSV', None)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password
)

filename = 'EQ{}{}{}'.format(TODAY.day,"{:02d}".format(TODAY.month),str(TODAY.year)[-2:])
URL = 'https://www.bseindia.com/download/BhavCopy/Equity/' + filename + '_CSV.ZIP'

try:
    r = requests.get(URL)
except:
    sys.exit()

open(PATH_TO_CSV + filename + '_CSV.ZIP', 'wb').write(r.content)

try:
     with ZipFile(PATH_TO_CSV + filename + '_CSV.ZIP', 'r') as zipObj:
         zipObj.extractall(path=PATH_TO_CSV)
except:
    os.remove(PATH_TO_CSV + filename + '_CSV.ZIP')
    sys.exit()

redis_client.flushall()

with open(PATH_TO_CSV + filename + '.CSV') as stocks_csv:
    csv_reader = csv.reader(stocks_csv, delimiter=',')
    for ind, row in enumerate(csv_reader):
        if ind != 0:
            redis_client.zadd('searchname', {row[1].strip(): 0.0})
            redis_client.zadd('name', {row[1].strip(): float(row[0])})
            redis_client.zadd('open', {float(row[0]): float(row[4])})
            redis_client.zadd('high', {float(row[0]): float(row[5])})
            redis_client.zadd('low', {float(row[0]): float(row[6])})
            redis_client.zadd('close', {float(row[0]): float(row[7])})

os.remove(PATH_TO_CSV + filename + '_CSV.ZIP')
os.remove(PATH_TO_CSV + filename + '.CSV')
