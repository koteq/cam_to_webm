import os
import shutil
import logging
import tarfile
import tempfile
import subprocess
from threading import Thread


class TarToWebmCompressor(object):
    @staticmethod
    def compress(filename):
        thread = Thread(target=TarToWebmCompressor._compress_non_blocking, args=(filename,))
        thread.start()

    @staticmethod
    def _compress_non_blocking(filename):
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
        vopts = "-c:v libvpx -quality good -cpu-used 0 -b:v 500k -qmin 4 -qmax 60 -bufsize 5000k -threads 1"
        input_images = os.path.join(tmp_dir, '%04d.jpg')
        hour_webm = filename + '.webm'
        null = '/dev/null'
        if os.name == 'nt':
            null = 'NUL'
        cmd1 = 'ffmpeg -y -v quiet -nostats -f image2 -i "%s" -pass 1 -f rawvideo %s %s' % (input_images, vopts, null)
        cmd2 = 'ffmpeg -y -v quiet -nostats -f image2 -i "%s" -pass 2 %s "%s"' % (input_images, vopts, hour_webm)
        try:
            subprocess.check_call(cmd1)
            subprocess.check_call(cmd2)
            os.remove(filename)
        except subprocess.CalledProcessError:
            logging.exception("Failed to compress %s file" % (filename,))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        # combine 1-hour movies to daily movies
        # combined_webm = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime('%Y-%m-%d.webm')
        # combined_webm = os.path.join(os.path.dirname(filename), combined_webm)
        # if not os.path.exists(combined_webm):
        #     try:
        #         os.rename(hour_webm, combined_webm)
        #     except:
        #         logging.exception("Failed to rename %s to %s" % (hour_webm, combined_webm))
        # else:
        #     combined_webm_tmp = combined_webm + ".tmp"
        #     cmd = 'mkvmerge --quiet --webm -o "%s" "%s" "+" "%s"' % (combined_webm_tmp, combined_webm, hour_webm)
        #     try:
        #         subprocess.check_call(cmd)
        #         os.remove(combined_webm)  # for windows os
        #         os.rename(combined_webm_tmp, combined_webm)
        #         os.remove(hour_webm)
        #     except subprocess.CalledProcessError:
        #         logging.exception("Failed to append %s to %s" % (hour_webm, combined_webm))
