# -*- coding: utf-8 -*-
import os
import logging
import logging.config
LOG_FILE = "wrt.log"

dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE
        }
    },
    "loggers": {
        "wrt": {
            "handlers": ["fileHandler"],
            "level": "DEBUG",
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}
logging.config.dictConfig(dictLogConfig)


def main(args):
    print(args)


def show(args):
    if args.follow:
        os.system("tail -f " + LOG_FILE)
    else:
        os.system("more " + LOG_FILE)
