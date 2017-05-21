import cyclone.web
import sys

from twisted.internet import reactor
from twisted.python import log


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Try modifying the server file!")

if __name__ == "__main__":
    application = cyclone.web.Application([
        (r"/", MainHandler)
    ], autoreload=True)

    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application)
    reactor.run()
