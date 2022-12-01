# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QObject, QCoreApplication, pyqtSignal, QThreadPool
from PyQt5.QtMultimedia import QSound
import time
import qdarkstyle
import preferences
import utils
import config as cfg
import updater
from logger import logger
from static.main_ui import Ui_MainWindow
import static.resources
from msg_boxes import MsgBox


class Worker(QObject):
	blacklist_signal = pyqtSignal(list)
	players_list_signal = pyqtSignal(list)
	snipers_signal = pyqtSignal(dict)
	new_release_signal = pyqtSignal(bool)


	def run(self):
		try:
			logger.debug("Worker started.")
			logger.debug(
				"""
				Current Config:
					APP_NAME = {app_name}
					APP_VERSION = {app_version}
					EVIL_MEDIATONIC = {evil_mediatonic}
					CASE_SENSITIVE = {case_sensitive}
				""".format(
					app_name = cfg.APP_NAME,
					app_version = cfg.APP_VERSION,
					evil_mediatonic = cfg.EVIL_MEDIATONIC,
					case_sensitive = cfg.CASE_SENSITIVE
				)
			)
			self.blacklist_signal.emit(utils.get_data("blacklist", []))
			self.new_release_signal.emit(utils.check_new_release())
			players_list = []
			index_list = [0]
			cached_line = ""
			playing = False
			username = None
			while not username:
				username = utils.get_username()
			logger.info("Buscando nueva partida...")
			while True:
				if playing:
					logger.info("Sigue jugando, durmiendo...")
					time.sleep(60)
					logger.info("Desperté.")
				game_founded, index_list, cached_line, playing = utils.find_new_game(index_list, cached_line, playing=playing)
				if game_founded:
					logger.info("Hay nueva partida, guardo lo previo y emito señal.")
					success = utils.update_prev_games_players(index_list[-1], username)
					if not success:
						logger.error("Error obteniendo la lista de jugadores previos.")
					players_list = utils.get_players(index_list[-1], username)
					self.players_list_signal.emit(players_list)
					snipers = utils.get_snipers(players_list)
					if snipers:
						self.snipers_signal.emit(snipers)
		except Exception as ex:
			logger.exception(ex)


class HomeWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		try:
			super().__init__()
			self.setupUi(self)
			self.ui_basic_config()
			self.run_worker()
			self.init_alerts()
		except Exception as ex:
			logger.exception(ex)


	def ui_basic_config(self):
		try:
			self.windowIcon = QIcon(":/static/icon.png")
			self.setWindowIcon(self.windowIcon)
			self.action_about.triggered.connect(
				lambda: MsgBox.question(
					self,
					title="Acerca de",
					text=cfg.ABOUT_STRING
					)
				)
			self.action_export_as_csv.triggered.connect(self.export_as_csv)
			self.action_export_blacklist.triggered.connect(self.export_blacklist)
			self.action_import_blacklist.triggered.connect(self.import_blacklist)
			self.action_exit.triggered.connect(QCoreApplication.instance().quit)
			self.action_preferences.triggered.connect(self.show_preferences)
			self.clear_blacklist_button.clicked.connect(self.clear_blacklist)
			self.remove_player_blacklist_button.clicked.connect(self.remove_player_blacklist)
			self.add_player_to_blacklist_button.clicked.connect(lambda: self.add_to_blacklist(selected_list="current"))
			self.add_suspect_to_blacklist_button.clicked.connect(lambda: self.add_to_blacklist(selected_list="suspects"))
			self.add_manually_button.clicked.connect(self.add_player_manually)
			self.show()
				
		except Exception as ex:
			logger.exception(ex)
			pass


	def show_preferences(self):
		try:
			self.preferences = preferences.PreferencesWindow()
			self.preferences.setWindowIcon(self.windowIcon)
			self.preferences.show()
		except Exception as ex:
			logger.exception(ex)


	def clear_blacklist(self):
		title = "Limpiar lista negra"
		if not self.blacklist_list:
			MsgBox.info(
				self,
				title=title,
				text="La lista negra está vacía."
				)
			return
		result = MsgBox.warning(
			self,
			title=title,
			text="¿Estás seguro de querer limpiar la lista negra?",
			inf_text="Esta acción no se puede deshacer.",
			return_result=True
			)
		if result:
			logger.info("Limpiando la blacklist.")
			success = utils.clear_blacklist()
			if not success:
				MsgBox.error(
					self,
					title=title,
					text="Hubo un error al eliminar el jugador."
				)
				return
			self.blacklist_list.clear()
			self.fill_snipers()


	def remove_player_blacklist(self):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Eliminar jugador de la lista negra")
		if not self.blacklist_list:
			msg_box.setIcon(QMessageBox.Information)
			msg_box.setText("La lista negra está vacía.")
			msg_box.setDefaultButton(QMessageBox.Close)
			msg_box.exec_()
			return
		if not self.blacklist_list.currentItem():
			msg_box.setIcon(QMessageBox.Information)
			msg_box.setText("Seleccione un jugador a eliminar.")
			msg_box.setDefaultButton(QMessageBox.Close)
			msg_box.exec_()
			return
		player_index = self.blacklist_list.currentRow()
		player_name = self.blacklist_list.currentItem().text()
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		buttonY = msg_box.button(QMessageBox.Yes)
		buttonY.setText("Eliminar")
		buttonN = msg_box.button(QMessageBox.No)
		buttonN.setText('Cancelar')
		msg_box.setText("¿Estás seguro de que quieres eliminar a '{}' de la lista negra?".format(player_name))
		msg_box.setInformativeText("Esta acción no se puede deshacer.")
		msg_box.setFixedSize(500, 500)
		result = msg_box.exec_()
		if result == QMessageBox.Yes:
			logger.info("Limpiando la blacklist.")
			success = utils.clear_blacklist(player=player_name)
			if not success:
				err_msg_box = QMessageBox(self)
				err_msg_box.setIcon(QMessageBox.Critical)
				err_msg_box.setWindowTitle("Eliminar jugador de la lista negra")
				err_msg_box.setDefaultButton(QMessageBox.Close)
				err_msg_box.setText("Hubo un error al limpiar la blacklist.")
				err_msg_box.exec_()
				return
			self.blacklist_list.takeItem(player_index)
		self.fill_snipers()


	def add_to_blacklist(self, selected_list=None, player_name=None):
		err_msg_box = QMessageBox(self)
		err_msg_box.setWindowTitle("Agregar a la lista negra")
		err_msg_box.setIcon(QMessageBox.Information)
		err_msg_box.setText("Seleccione un jugador a agregar.")
		err_msg_box.setDefaultButton(QMessageBox.Close)
		if selected_list:
			if selected_list == "current":
				if not self.current_game_players_list.currentItem():
					err_msg_box.exec_()
					return
				player_name = self.current_game_players_list.currentItem().text()
			elif selected_list == "suspects":
				if not self.suspects_list.currentItem():
					err_msg_box.exec_()
					return
				player_index = self.suspects_list.currentRow()
				player_name = self.suspects_list.currentItem().text()
				self.suspects_list.takeItem(player_index)
		success, blacklist = utils.save_to_blacklist(player_name)
		if not success:
			err_msg_box = QMessageBox(self)
			err_msg_box.setIcon(QMessageBox.Critical)
			err_msg_box.setWindowTitle("Agregar a la lista negra")
			err_msg_box.setDefaultButton(QMessageBox.Close)
			err_msg_box.setText("Hubo un error al guardar en la blacklist.")
			err_msg_box.exec_()
			return
		self.fill_blacklist(blacklist)
		self.fill_snipers()


	def add_player_manually(self):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Agregar a la lista negra")
		player, ok = QInputDialog.getText(
			msg_box,
			"Agregar sniper",
			"Ingrese el nombre del sniper",
			QLineEdit.Normal
		)
		if ok and player:
			self.add_to_blacklist(player_name=player)


	def run_worker(self):
		# QThread object to run daemon subprocess.
		self.thread = QThread()
		self.worker = Worker()
		# Move daemon to the thread.
		self.worker.moveToThread(self.thread)
		# Connect signals and slots.
		self.thread.started.connect(self.worker.run)
		self.worker.blacklist_signal.connect(self.fill_blacklist)
		self.worker.players_list_signal.connect(self.fill_players)
		self.worker.snipers_signal.connect(lambda: self.fill_snipers(first=True))
		self.worker.new_release_signal.connect(self.check_new_release)
		self.thread.start()


	def fill_players(self, players_list):
		self.clear_players_lists()
		logger.info("Llenando la lista con los nuevos jugadores.")
		for player in players_list:
			self.current_game_players_list.addItem(player)


	def fill_blacklist(self, blacklist):
		self.blacklist_list.clear()
		logger.info("Llenando la blacklist.")
		logger.debug(blacklist)
		for item in blacklist:
			self.blacklist_list.addItem(item)


	def fill_snipers(self, data=None, first=False):
		if not data:
			players_list = [self.current_game_players_list.item(i).text() for i in range(self.current_game_players_list.count())]
			data = utils.get_snipers(players_list)
		self.clear_snipers()
		logger.info("Llenando la lista de snipers.")
		snipers = data.get("snipers", [])
		suspects = data.get("suspects", [])
		logger.debug("Snipers: {}".format(snipers))
		for sniper in data.get("snipers", []):
			self.snipers_list.addItem(sniper)
		logger.info("Llenando la lista de posibles snipers.")
		logger.debug("Posibles snipers: {}".format(suspects))
		for suspect in suspects:
			self.suspects_list.addItem(suspect)
		if first:
			if data.get("snipers"):
				msg_box = QMessageBox(self)
				msg_box.setWindowTitle("Snipers detectados")
				msg_box.setIcon(QMessageBox.Warning)
				msg_box.setText("Se han encontrado snipers en la partida.")
				msg_box.setDefaultButton(QMessageBox.Close)
				self.play_sound()
				msg_box.exec_()


	def clear_snipers(self):
		logger.info("Limpiando la lista de snipers antigua.")
		self.snipers_list.clear()
		logger.info("Limpiando la lista de posibles snipers antigua.")
		self.suspects_list.clear()


	def clear_players_lists(self):
		logger.info("Limpiando lista anterior de jugadores.")
		self.current_game_players_list.clear()
		self.suspects_list.clear()


	def check_new_release(self, new_release):
		if new_release:
			msg_box = QMessageBox(self)
			msg_box.setWindowTitle("Nueva versión")
			msg_box.setIcon(QMessageBox.Information)
			msg_box.setText("Se ha encontrado una nueva versión de la aplicación.")
			msg_box.setInformativeText("¿Desea descargarla?")
			msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			buttonY = msg_box.button(QMessageBox.Yes)
			buttonY.setText("Descargar")
			buttonN = msg_box.button(QMessageBox.No)
			buttonN.setText("Quizá más tarde")
			result = msg_box.exec_()
			if result == QMessageBox.Yes:
				msg_box.setText("Se descargará la ultima versión en segundo plano.")
				msg_box.setInformativeText("Sea paciente, se le avisará cuando termine.")
				msg_box.setStandardButtons(QMessageBox.Ok)
				msg_box.exec_()
				worker = updater.Update()
				worker.signals.success_signal.connect(self.show_updater_results)
				QThreadPool.globalInstance().start(worker)


	def show_updater_results(self, success, result):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Descargar")
		msg_box.setIcon(QMessageBox.Information)
		msg_box.setDefaultButton(QMessageBox.Close)
		if not success:
			msg_box.setIcon(QMessageBox.Warning)
			msg_box.setText(result)
			msg_box.exec_()
			return
		msg_box.setText("Éxito al descargar la ultima versión.\nUbicación: {}".format(result))
		msg_box.setInformativeText("Puede eliminar esta versión si lo desea.")
		msg_box.exec_()
		return


	def export_as_csv(self):
		data = {}
		data["method"] = "export"
		blacklist = [self.blacklist_list.item(i).text() for i in range(self.blacklist_list.count())]
		players = [self.current_game_players_list.item(i).text() for i in range(self.current_game_players_list.count())]
		suspects = [self.suspects_list.item(i).text() for i in range(self.suspects_list.count())]
		snipers =  [self.snipers_list.item(i).text() for i in range(self.snipers_list.count())]
		path = QFileDialog.getSaveFileName(
			self,
			caption = "Guardar archivo",
			filter = "Archivo CSV (*.csv)"
			)[0]
		if path:
			success = utils.export_as_csv(path, blacklist, players, suspects, snipers)
			data["success"] = success
			data["path"] = path
			self.show_file_result(data)


	def export_blacklist(self):
		data = {}
		data["method"] = "export"
		blacklist = [self.blacklist_list.item(i).text() for i in range(self.blacklist_list.count())]
		path = QFileDialog.getSaveFileName(
			self,
			caption = "Exportar lista negra",
			filter = "Archivo de texto (*.txt)"
			)[0]
		if path:
			success = utils.export_blacklist(path, blacklist)
			data["success"] = success
			data["path"] = path
			self.show_file_result(data)


	def import_blacklist(self):
		data = {}
		data["method"] = "import"
		path = QFileDialog.getOpenFileName(
			self,
			caption = "Importar lista negra",
			filter = "Archivo de texto (*.txt)"
			)[0]
		if path:
			success, blacklist = utils.import_blacklist(path)
			data["success"] = success
			data["path"] = path
			self.show_file_result(data)
			self.fill_blacklist(blacklist)
			self.fill_snipers()


	def show_file_result(self, data):
		method = data.get("method")
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("{}".format(
				"Exportar" if method == "export" else "Importar"
			))
		msg_box.setIcon(QMessageBox.Information)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setText("¡Archivo {}!".format(
			"exportado" if method == "export" else "importado"
		))
		msg_box.setInformativeText("Ubicación: {}".format(data["path"])) if data.get("path") else msg_box.setInformativeText("")
		if not data.get("success"):
			msg_box.setIcon(QMessageBox.Critical)
			msg_box.setText("Hubo un error al {} el archivo.".format(
				"exportar" if method == "export" else "importar"
			))
			msg_box.setInformativeText("")
		msg_box.exec_()


	def play_sound(self):
		try:
			audio_to_play = ":/static/sniper_detected.wav"
			if utils.get_data("preferences", {}).get("audio_checked", False):
				path = utils.get_data("preferences").get("audio_file_path")
				if path:
					if os.path.exists(path):
						logger.info("El archivo existe.")
						audio_to_play = path
					else:
						logger.error("El archivo no existe, uso el que tengo por defecto.")
				sound = QSound(audio_to_play, self)
				sound.play()
		except Exception as ex:
			logger.exception(ex)
			logger.error("Hubo un error al reproducir el archivo.")
			pass


	def init_alerts(self):
		data = utils.get_data()
		data["preferences"] = data.get("preferences", {})
		if cfg.EVIL_MEDIATONIC:
			if not data["preferences"].get("hide_evil_mt_alert"):
				hide_alert = MsgBox.warning(
					self,
					title="Aviso",
					text="Mediatonic modificó los logs y los nombres no se muestran en su totalidad,\n"
						"por lo tanto, los nombres en la aplicacion se mostrarán con las últimas 3 letras.\n"
						"Puedes agregar los nombres manualmente en el botón '+', o buscar por las últimas 3 letras en la lista de jugadores.",
					inf_text="Nota: <b>La aplicación tendrá en cuenta mayúsculas y minúsculas</b>",
					return_result=True,
					yes="No volver a mostrar",
					no="Recordármelo"
				)
				if hide_alert:
					data["preferences"]["hide_evil_mt_alert"] = True
					utils.save_data(data)


def main():
	try:
		utils.clear_log()
		logger.debug("Comienza Fall Guys Anti Sniper v{}".format(cfg.APP_VERSION))
		app = QApplication(sys.argv)
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
		HomeWindow()
		app.exec_()
	except Exception as ex:
		logger.exception(ex)

if __name__ == "__main__":
	main()
