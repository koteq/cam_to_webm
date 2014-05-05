import time
import base64
import socket
import httplib
import logging
import urlparse
from StringIO import StringIO

from modules.event import Event


class CameraPooler(httplib.HTTPConnection):
    def __init__(self, url, timeout=1.0):
        logging.debug("CameraPooler init")
        url = urlparse.urlparse(url)
        httplib.HTTPConnection.__init__(self, host=url.hostname, port=url.port, timeout=timeout)
        self.path = url.path
        self.basic_auth = "Basic " + base64.encodestring(url.username + ":" + url.password)[:-1]
        self.on_frame = Event()

    def start_pooling_loop(self, interval):
        while True:
            start_time = time.clock()
            frame = self._get_frame()
            self.on_frame(frame)
            sleep_time = min(interval, interval - (time.clock() - start_time))
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _get_frame(self):
        try:
            self.putrequest("GET", self.path)
            self.putheader("Authorization", self.basic_auth)
            self.endheaders()
            response = self.getresponse()
            return StringIO(response.read())
        except socket.timeout:
            logging.warning("Connection timeout")
        except Exception as e:
            logging.exception("Connection problem: %s" % (e,))
        finally:
            self.close()
