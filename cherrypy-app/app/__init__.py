import cherrypy
import os
import redis

from dotenv import load_dotenv
load_dotenv()

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)
redis_client = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
)

class BSEStocks(object):
    @cherrypy.expose
    def index(self):
        index_template = env.get_template('index.html')
        stocks = redis_client.zrevrangebyscore('close', '+inf', '-inf', start=0, num=10)
        data = [{} for el in stocks]
        for ind, stock in enumerate(stocks):
            stock_no = float(stock.decode())
            data[ind]['code'] = int(float(stock.decode()))
            data[ind]['name'] = redis_client.zrangebyscore('name', stock_no, stock_no + 1)[0].decode()
            data[ind]['open'] = redis_client.zscore('open', float(stock.decode()))
            data[ind]['high'] = redis_client.zscore('high', float(stock.decode()))
            data[ind]['low'] = redis_client.zscore('low', float(stock.decode()))
            data[ind]['close'] = redis_client.zscore('close', float(stock.decode()))
        return index_template.render(data=data)

    @cherrypy.expose
    def search(self, query):
        template = env.get_template('search.html')
        min_r = '[' + query.upper()
        max_r = '[' + query.upper() + '\xff'
        stocks = redis_client.zrangebylex('searchname', min_r, max_r)
        data = [{} for el in stocks]
        for ind, stock in enumerate(stocks):
            stock_no = redis_client.zscore('name', stock.decode())
            data[ind]['code'] = int(stock_no)
            data[ind]['name'] = stock.decode()
            data[ind]['open'] = redis_client.zscore('open', stock_no)
            data[ind]['high'] = redis_client.zscore('high', stock_no)
            data[ind]['low'] = redis_client.zscore('low', stock_no)
            data[ind]['close'] = redis_client.zscore('close', stock_no)
        return template.render(search_query=query, data=data)

