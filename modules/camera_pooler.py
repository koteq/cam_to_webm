import base64
import socket
import httplib
import logging
import urlparse


class CameraPooler(httplib.HTTPConnection):
    def __init__(self, url, timeout=1.0, attempts=3):
        logging.debug("CameraPooler init")
        url = urlparse.urlparse(url)
        httplib.HTTPConnection.__init__(self, url.hostname, url.port, timeout)
        self.path = url.path
        self.attempts = attempts
        self.basic_auth = "Basic " + base64.encodestring(url.username + ":" + url.password)[:-1]

    def pool(self):
        self.close()
        self.putrequest("GET", self.path)
        self.putheader("Authorization", self.basic_auth)
        for i in range(self.attempts):
            try:
                self.endheaders()
                return self.getresponse()
            except socket.timeout:
                logging.debug("Connection timeout")
            except (httplib.HTTPException, socket.error):
                logging.warning("Connection problem", exc_info=True)
                break
