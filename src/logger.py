import logging
import os

logging.basicConfig(
	filename='application.log',
	encoding='utf-8',
	level=logging.DEBUG,
	format="%(asctime)s MODULE: %(module)s (%(funcName)s) - LINE: %(lineno)d - %(levelname)s - %(message)s",
	datefmt='%d/%m/%Y %H:%M:%S'
	)

logger = logging.getLogger(__name__)