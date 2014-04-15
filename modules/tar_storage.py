import os
import tarfile
import logging
from datetime import datetime
from StringIO import StringIO


class TarStorage(object):
    """Stores added jpegs in archives"""
    tar = None
    bufsize = 1048576  # 1Mb
    current_image_num = 1
    current_archive_name = None
    image_name_format = "%04d.jpg"
    archive_name_format = "%Y-%m-%d %H.tar.mjpeg"

    def __init__(self, path):
        logging.debug("TarStorage init")
        self.path = os.path.realpath(path)

    def __del__(self):
        if not self.tar is None:
            logging.debug("File closed on exit")
            self.tar.close()

    def store(self, fileobj):
        if fileobj is None or not hasattr(fileobj, "read"):
            logging.warn("Invalid fileobj specified")
            return
        jpeg = StringIO(fileobj.read())
        name = datetime.now().strftime(self.image_name_format % self.current_image_num)
        info = tarfile.TarInfo(name)
        info.size = jpeg.len
        if self._init_archive():
            try:
                self.tar.addfile(info, jpeg)
                self.current_image_num += 1
            except (tarfile.TarError, IOError):
                logging.exception("Failed to add file to archive")

    def _init_archive(self):
        archive_name = datetime.now().strftime(self.archive_name_format)
        if self.current_archive_name is None or not self.current_archive_name == archive_name:
            self.current_image_num = 1
            self.current_archive_name = archive_name
            filename = os.path.join(self.path, archive_name)
            logging.info("TarStorage output goes to %s" % filename)
            try:
                self.tar = tarfile.open(filename, "w|", bufsize=self.bufsize)
            except (tarfile.TarError, IOError):
                logging.exception("Failed to open %s" % filename)
                self.tar = None
                self.current_archive_name = None
                return False
        return True
