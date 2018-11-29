import logging
import logging.config
import time

logger = logging.getLogger(name=__name__)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': "calculation_log.log".format(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())),
            'mode': 'w',
        }
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
    'loggers': {
    },
    'console':{

    },
}

def configure_logging():
    logging.config.dictConfig(config=LOGGING_CONFIG)
