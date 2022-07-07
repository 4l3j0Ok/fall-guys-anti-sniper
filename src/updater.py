import os
import shutil
from zipfile import ZipFile
import requests
import utils
import config
from logger import logger
import json
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject


class UpdaterSignals(QObject):
	success_signal = pyqtSignal(bool, str)


class Update(QRunnable):
	def __init__(self):
		super().__init__()
		self.signals = UpdaterSignals()
	def run(self):
		try:
			success, version = utils.get_latest_version()
			if not success:
				self.signals.success_signal.emit(False, version)
				return
			dirname = "FGAntiSniper-{}".format(version)
			path = os.path.join(os.getcwd(), dirname)
			if os.path.exists(path):
				logger.info("La carpeta ya esta creada, la borro.")
				shutil.rmtree(path)
			os.mkdir(path)
			response = requests.get(config.GITHUB_RELEASE_DOWNLOAD_URL.format(version))
			if not response:
				self.signals.success_signal.emit(False, config.ERR_CONNECTION)
				return
			zipfile_name = os.path.join(path, dirname + ".zip")
			open(zipfile_name, "wb").write(response.content)
			ZipFile(zipfile_name, "r").extractall(path)
			os.remove(zipfile_name)
			success = self.move_data(path)
			logger.warning("Result move_data: {}".format(success))
			self.signals.success_signal.emit(True, path)
			return
		except Exception as ex:
			logger.exception(ex)
			self.signals.success_signal.emit(False, config.ERR_UPDATER_EXCEPTION)
			return

	def move_data(self, dest_path):
		if os.path.exists(config.DATA_PATH):
			with open(dest_path + "\\data.json", "w+") as file:
				json.dump(
					json.load(open(config.DATA_PATH, "r")),
					file)
				return True
		return False
