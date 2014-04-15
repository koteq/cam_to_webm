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
    storage = TarStorage('archives')

    storage.on_storage_closed.add_handler(TarToWebmCompressor.compress)
    pooler.on_response.add_handler(storage.store)

    pooler.start_pooling_loop(interval=5.0)


if __name__ == "__main__":
    main()
