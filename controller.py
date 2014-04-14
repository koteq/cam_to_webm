import time
import logging
import logging.config
from camera_pooler import CameraPooler
from tar_storage import TarStorage


def start_loop(delay, action):
    """Call action func every delay seconds (synch)"""
    while True:
        elapsed = time.clock()
        try:
            action()
        except Exception:
            logging.exception('Something went wrong')
        elapsed = time.clock() - elapsed
        time.sleep(delay - elapsed % delay)


def main():
    logging.config.fileConfig('logging.ini')
    with file('camera_image.url') as f:
        camera_image_url = f.read()

    pooler = CameraPooler(camera_image_url)
    storage = TarStorage('archives')

    start_loop(5, lambda: storage.store(pooler.pool()))


if __name__ == "__main__":
    main()
