import os
import tarfile
import logging
from datetime import datetime

from modules.event import Event


class TarStorage(object):
    """Stores added jpegs in archives"""
    tar = None
    bufsize = 1048576  # 1Mb
    no_response_num = 0
    max_no_response_frames = 60  # 3 seconds
    current_file_num = 1
    current_archive_name = None
    file_name_format = "%04d.jpg"
    archive_name_format = "%Y-%m-%d %H.tar.mjpeg"

    def __init__(self, path, no_response_file=None):
        logging.debug("TarStorage init")
        self.path = os.path.realpath(path)
        self.no_response_file = os.path.realpath(no_response_file)
        self.on_storage_closed = Event()

    def __del__(self):
        if not self.tar is None:
            logging.debug("File closed on exit")
            self.tar.close()
            self.on_storage_closed(os.path.join(self.path, self.current_archive_name))

    def store(self, frame):
        if self._init_archive():
            if frame is not None:
                self.no_response_num = 0
                self._addfile_to_archive(frame)
            else:
                if self.no_response_file is not None and self.no_response_num < self.max_no_response_frames:
                    try:
                        with open(self.no_response_file, "rb") as fileobj:
                            self._addfile_to_archive(fileobj)
                    except:
                        logging.exception("Failed to add no_response_file to archive")
                self.no_response_num += 1

    def _addfile_to_archive(self, fileobj):
        name = self.file_name_format % (self.current_file_num,)
        info = tarfile.TarInfo(name)
        fileobj.seek(0, os.SEEK_END)
        info.size = fileobj.tell()
        fileobj.seek(0)
        try:
            self.tar.addfile(info, fileobj)
            self.current_file_num += 1
        except (tarfile.TarError, IOError):
            logging.exception("Failed to add file to archive")

    def _init_archive(self):
        archive_name = datetime.now().strftime(self.archive_name_format)
        if self.current_archive_name is None or not self.current_archive_name == archive_name:
            if not self.tar is None:
                self.tar.close()
                self.on_storage_closed(os.path.join(self.path, self.current_archive_name))
            self.no_response_num = 0
            self.current_file_num = 1
            self.current_archive_name = archive_name
            filename = os.path.join(self.path, archive_name)
            logging.info("TarStorage output goes to %s" % filename)
            try:
                # TODO: continue archive if it's was modified recently
                # TODO: otherwise start it over
                self.tar = tarfile.open(filename, "w|", bufsize=self.bufsize)
            except (tarfile.TarError, IOError):
                logging.exception("Failed to open %s" % filename)
                self.tar = None
                self.current_archive_name = None
                return False
        return True
