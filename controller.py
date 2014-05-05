import logging
import logging.config

from modules.camera_pooler import CameraPooler
from modules.tar_storage import TarStorage
from modules.tar_to_webm_compressor import TarToWebmCompressor


def main():
    logging.config.fileConfig('logging.ini')
    with file('camera_image.url') as f:
        camera_image_url = f.read()

    pooler = CameraPooler(camera_image_url)
    storage = TarStorage(path='archives', no_response_file='no_signal.jpg')

    pooler.on_frame.add_handler(storage.store)
    storage.on_storage_closed.add_handler(TarToWebmCompressor.compress)

    pooler.start_pooling_loop(interval=2.4)  # 25 fps, 1 min real time = 1 sec video time


if __name__ == "__main__":
    main()
