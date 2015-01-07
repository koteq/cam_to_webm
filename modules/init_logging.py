import logging
import logging.config


def init_logging(file=None, file_level=logging.DEBUG, stdout=True):
    config = {
        'version': 1,
        'formatters': {
            'consoleFormatter': {
                'format': '%(levelname)s %(message)s'
            },
            'fileFormatter': {
                'format': '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s'
            },
        },
        'handlers': {
            'consoleHandler': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'consoleFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {
                'handlers': [],
                'level': 'DEBUG',
            }
        }
    }
    if file is not None:
        config['handlers']['fileHandler'] = {
            'level': file_level,
            'class': 'logging.FileHandler',
            'formatter': 'fileFormatter',
            'filename': file,
        }
        config['loggers']['']['handlers'].append('fileHandler')
    if stdout:
        config['loggers']['']['handlers'].append('consoleHandler')
    logging.config.dictConfig(config)
