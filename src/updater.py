import os
import shutil
from zipfile import ZipFile
import requests
import utils
import config
from logger import logger
import json


def update():
	try:
		success, version = utils.get_latest_version()
		if not success:
			return False, version
		dirname = "FGAntiSniper-{}".format(version)
		path = os.path.join(os.getcwd(), dirname)
		if os.path.exists(path):
			logger.info("La carpeta ya esta creada, la borro.")
			shutil.rmtree(path)
		os.mkdir(path)
		response = requests.get(config.GITHUB_RELEASE_DOWNLOAD_URL.format(version))
		if not response:
			return False, config.ERR_CONNECTION
		zipfile_name = os.path.join(path, dirname + ".zip")
		open(zipfile_name, "wb").write(response.content)
		ZipFile(zipfile_name, "r").extractall(path)
		os.remove(zipfile_name)
		success = move_data(path)
		logger.warning("Result move_data: {}".format(success))
		return True, path
	except Exception as ex:
		logger.exception(ex)
		return False, config.ERR_UPDATER_EXCEPTION

def move_data(dest_path):
	if os.path.exists(config.DATA_PATH):
		with open(dest_path + "\\data.json", "w+") as file:
			json.dump(
				json.load(open(config.DATA_PATH, "r")),
				file)
			return True
	return False
