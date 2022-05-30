# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QObject, QCoreApplication, pyqtSignal
import time
import webbrowser
import qdarkstyle
import utils
import config
from static.ui import Ui_MainWindow
import static.resources
from logger import logger


class Worker(QObject):
	blacklist_signal = pyqtSignal(list)
	players_list_signal = pyqtSignal(list)
	snipers_signal = pyqtSignal(dict)
	new_release_signal = pyqtSignal(bool)


	def run(self):
		try:
			self.blacklist_signal.emit(utils.get_data().get("blacklist", []))
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
			self.show()
			self.run_worker()
		except Exception as ex:
			logger.exception(ex)


	def ui_basic_config(self):
		try:
			self.windowIcon = QIcon(":/static/icon.png")
			self.setWindowIcon(self.windowIcon)
			self.action_about.triggered.connect(self.show_about)
			self.action_export.triggered.connect(self.export)
			self.action_exit.triggered.connect(QCoreApplication.instance().quit)
			self.clear_blacklist_button.clicked.connect(self.clear_blacklist)
			self.remove_player_blacklist_button.clicked.connect(self.remove_player_blacklist)
			self.add_player_to_blacklist_button.clicked.connect(lambda: self.add_to_blacklist(selected_list="current"))
			self.add_suspect_to_blacklist_button.clicked.connect(lambda: self.add_to_blacklist(selected_list="suspects"))
			self.add_manually_button.clicked.connect(self.add_player_maually)
		except Exception as ex:
			logger.exception(ex)


	def show_about(self):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Acerca de")
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setText(config.ABOUT_STRING)
		msg_box.exec_()


	def export(self):
		blacklist = [self.blacklist_list.item(i).text() for i in range(self.blacklist_list.count())]
		players = [self.current_game_players_list.item(i).text() for i in range(self.current_game_players_list.count())]
		suspects = [self.suspects_list.item(i).text() for i in range(self.suspects_list.count())]
		snipers =  [self.snipers_list.item(i).text() for i in range(self.snipers_list.count())]
		path = utils.export_as_csv(blacklist, players, suspects, snipers)
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Exportar")
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setText("Archivo exportado!")
		msg_box.setInformativeText("Ubicación: {}".format(path))
		if not path:
			msg_box.setIcon(QMessageBox.Critical)
			msg_box.setText("Hubo un error al exportar el archivo.")
			msg_box.setInformativeText("")
		msg_box.exec_()



	def clear_blacklist(self):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Limpiar lista negra")
		if not self.blacklist_list:
			msg_box.setIcon(QMessageBox.Information)
			msg_box.setText("La lista negra está vacía.")
			msg_box.setDefaultButton(QMessageBox.Close)
			msg_box.exec_()
			return
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		buttonY = msg_box.button(QMessageBox.Yes)
		buttonY.setText("Limpiar")
		buttonN = msg_box.button(QMessageBox.No)
		buttonN.setText('Cancelar')
		msg_box.setText("¿Estás seguro de querer limpiar la lista negra?")
		msg_box.setInformativeText("Esta acción no se puede deshacer.")
		msg_box.setFixedSize(500, 500)
		result = msg_box.exec_()
		if result == QMessageBox.Yes:
			logger.info("Limpiando la blacklist.")
			success = utils.clear_blacklist()
			if not success:
				err_msg_box = QMessageBox(self)
				err_msg_box.setIcon(QMessageBox.Critical)
				err_msg_box.setWindowTitle("Limpiar lista negra")
				err_msg_box.setDefaultButton(QMessageBox.Close)
				err_msg_box.setText("Hubo un error al eliminar el jugador.")
				err_msg_box.exec_()
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
		buttonY.setText("Limpiar")
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
		current_blacklist = [self.blacklist_list.item(i).text() for i in range(self.blacklist_list.count())]
		if player_name not in current_blacklist:
			success = utils.save_to_blacklist(player_name)
			if not success:
				err_msg_box = QMessageBox(self)
				err_msg_box.setIcon(QMessageBox.Critical)
				err_msg_box.setWindowTitle("Agregar a la lista negra")
				err_msg_box.setDefaultButton(QMessageBox.Close)
				err_msg_box.setText("Hubo un error al guardar en la blacklist.")
				err_msg_box.exec_()
				return
			self.blacklist_list.addItem(player_name)
			self.fill_snipers()


	def add_player_maually(self):
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
				webbrowser.open(config.LATEST_RELEASE_URL)


def main():
	try:
		app = QApplication(sys.argv)
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
		home = HomeWindow()
		app.exec_()
	except Exception as ex:
		logger.exception(ex)

if __name__ == "__main__":
	main()