import os
import logging
import tarfile
import tempfile
import subprocess


class TarToWebmCompressor(object):
    @staticmethod
    def compress(filename):
        tmp_dir = tempfile.mkdtemp()
        tar = tarfile.open(filename, "r|")
        tar.extractall(tmp_dir)
        vopts = "-c:v libvpx -quality good -cpu-used 0 -b:v 500k -qmin 4 -qmax 60 -bufsize 5000k -threads 1"
        #vopts += "-vf scale=-1:480"
        try:
            input = os.path.join(tmp_dir, '%04d.jpg')
            output = filename + '.webm'
            pass1 = 'ffmpeg -y -v quiet -nostats -pass 1 -f image2 -i "%s" -f rawvideo %s /dev/null' % (input, vopts)
            pass2 = 'ffmpeg -y -v quiet -nostats -pass 2 -f image2 -i "%s" %s "%s"' % (input, vopts, output)
            subprocess.check_call(pass1)
            subprocess.check_call(pass2)
        except subprocess.CalledProcessError:
            logging.exception("Failed to compress %s file" % (filename,))
        finally:
            os.removedirs(tmp_dir)