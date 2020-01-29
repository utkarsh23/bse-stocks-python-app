import cherrypy
from app import BSEStocks

app = cherrypy.tree.mount(BSEStocks(), '/')

if __name__=='__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })
    cherrypy.quickstart(BSEStocks())
