import os
import shutil
import logging
import tarfile
import tempfile
import subprocess
import distutils.spawn
from threading import Thread

if not distutils.spawn.find_executable('ffmpeg'):
    raise ImportError('ffmpeg executable not found')


class TarToH264Compressor(object):
    fps = 20
    scale = '-1:360'
    bitrate = '66k'

    @classmethod
    def compress(cls, filename, *args, **kvargs):
        thread = Thread(target=cls._compress, args=(filename,))
        thread.start()

    @classmethod
    def _compress(cls, filename):
        # extract tar
        tmp_dir = tempfile.mkdtemp()
        try:
            tar = tarfile.open(filename, "r|")
            tar.extractall(tmp_dir)
            tar.close()
        except:
            logging.exception("Failed extract %s file" % (filename,))
            os.rmdir(tmp_dir)
            return

        # compress images into web movie
        vopts = "-vf scale=" + cls.scale + " -c:v libx264 -preset slow -movflags faststart -b:v " + cls.bitrate
        input_images = os.path.join(tmp_dir, '%04d.jpg')
        hour_mp4 = filename + '.mp4'
        null = '/dev/null'
        if os.name == 'nt':
            null = 'NUL'
        cmd1 = 'ffmpeg -y -f image2 -r %d -i "%s" -pass 1 -f mp4 %s %s' % (cls.fps, input_images, vopts, null)
        cmd2 = 'ffmpeg -y -f image2 -r %d -i "%s" -pass 2 %s "%s"' % (cls.fps, input_images, vopts, hour_mp4)
        try:
            subprocess.check_call(cmd1, cwd=tmp_dir, shell=True)
            subprocess.check_call(cmd2, cwd=tmp_dir, shell=True)
            os.remove(filename)
        except subprocess.CalledProcessError:
            logging.exception("Failed to compress %s file" % (filename,))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
