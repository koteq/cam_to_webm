import os
import logging
import datetime


class ArchiveRotation(object):
    def __init__(self, path, ext, max_age):
        self.path = os.path.realpath(path)
        self.ext = ext
        self.max_age = max_age

    def rotate(self, *args, **kvargs):
        for file in os.listdir(self.path):
            file = os.path.join(self.path, file)
            filename, ext = os.path.splitext(file)
            if ext == self.ext:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                if datetime.datetime.now() - mtime > self.max_age:
                    logging.info("Removing old file %s" % (file,))
                    os.remove(file)
