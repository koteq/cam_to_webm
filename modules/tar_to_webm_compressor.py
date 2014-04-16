import os
import logging
import tarfile
import tempfile
import datetime
import subprocess


class TarToWebmCompressor(object):

    @staticmethod
    def compress(filename):
        # extract tar
        tmp_dir = tempfile.mkdtemp()
        try:
            tar = tarfile.open(filename, "r|")
            tar.extractall(tmp_dir)
            tar.close()
        except:
            logging.exception("Failed extract %s file" % (filename,))
            os.removedirs(tmp_dir)
            return

        # compress images into web movie
        vopts = "-c:v libvpx -quality good -cpu-used 0 -b:v 500k -qmin 4 -qmax 60 -bufsize 5000k -threads 1"
        #vopts += "-vf scale=-1:480"
        input_images = os.path.join(tmp_dir, '%04d.jpg')
        hour_webm = filename + '.webm'
        cmd1 = 'ffmpeg -y -v quiet -nostats -pass 1 -f image2 -i "%s" -f rawvideo %s /dev/null' % (input_images, vopts)
        cmd2 = 'ffmpeg -y -v quiet -nostats -pass 2 -f image2 -i "%s" %s "%s"' % (input_images, vopts, hour_webm)
        try:
            subprocess.check_call(cmd1)
            subprocess.check_call(cmd2)
            os.remove(filename)
        except subprocess.CalledProcessError:
            logging.exception("Failed to compress %s file" % (filename,))
        finally:
            os.removedirs(tmp_dir)

        # combine 1-hour movies to daily movies
        combined_webm = (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime('%Y-%m-%d.webm')
        combined_webm = os.path.join(os.path.dirname(filename), combined_webm)
        if not os.path.exists(combined_webm):
            try:
                os.rename(hour_webm, combined_webm)
            except:
                logging.exception("Failed to rename %s to %s" % (hour_webm, combined_webm))
        else:
            cmd = 'mkvmerge -o "%s" --webm --display-dimensions "0:640x480" -d 0 "+" %s' % (combined_webm, hour_webm)
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError:
                logging.exception("Failed to append %s to %s" % (hour_webm, combined_webm))
