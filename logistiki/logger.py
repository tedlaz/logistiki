import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = "%(asctime)s|%(filename)s:%(lineno)d(%(levelname)s)> %(message)s"
formatter = logging.Formatter(fmt)
file_handler = logging.FileHandler("logistiki.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# logger.info('this is a test message')
# logger.critical('skata sto isioma')
# logger.debug('Δοκιμή για τους κάλους')
# CRITICAL	50
# ERROR	    40
# WARNING	30
# INFO	    20
# DEBUG	    10
