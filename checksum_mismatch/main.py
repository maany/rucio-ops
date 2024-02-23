import logging 
import logging
import colorlog

logger = logging.getLogger(__name__)

def main():
    logger.info("Hello, world!")

if __name__ == '__main__':
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s:%(name)s:%(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    main()


