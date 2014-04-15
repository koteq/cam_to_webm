import time
import base64
import socket
import httplib
import logging
import urlparse

from modules.event import Event


class CameraPooler(httplib.HTTPConnection):
    def __init__(self, url, timeout=1.0):
        logging.debug("CameraPooler init")
        url = urlparse.urlparse(url)
        httplib.HTTPConnection.__init__(self, url.hostname, url.port, timeout)
        self.path = url.path
        self.basic_auth = "Basic " + base64.encodestring(url.username + ":" + url.password)[:-1]
        self.on_response = Event()

    def start_pooling_loop(self, interval):
        while True:
            elapsed = time.clock()
            responce = self._pool()
            self.on_response(responce)
            elapsed = time.clock() - elapsed
            time.sleep(interval - elapsed % interval)

    def _pool(self):
        self.close()
        self.putrequest("GET", self.path)
        self.putheader("Authorization", self.basic_auth)
        try:
            self.endheaders()
            return self.getresponse()
        except socket.timeout:
            logging.debug("Connection timeout")
        except (httplib.HTTPException, socket.error):
            logging.warning("Connection problem", exc_info=True)
