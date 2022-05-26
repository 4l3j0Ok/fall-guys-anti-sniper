# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import utils
import config
from logger import logger


#TODO Send windows notification if sniper detected https://www.youtube.com/watch?v=p1w-FZclhXs

class Daemon(QObject):
	blacklist_signal = pyqtSignal(list)
	players_list_signal = pyqtSignal(list)
	snipers_signal = pyqtSignal(dict)


	def run(self):
		blacklist = utils.get_data().get("blacklist", [])
		self.blacklist_signal.emit(blacklist)
		players_list = []
		index_list = [0]
		cached_line = ""
		playing = False
		username = None
		while not username:
			username = utils.get_username()
		logger.info("Buscando nueva partida...")
		while True:
			game_founded, index_list, cached_line, playing = utils.find_new_game(index_list, cached_line, playing=playing)
			if game_founded:
				logger.info("Hay nueva partida, guardo lo previo y emito señal.")
				utils.update_prev_games_players(index_list[-1], username)
				players_list = utils.get_players(index_list[-1], username)
				self.players_list_signal.emit(players_list)
				snipers = utils.get_snipers(players_list, blacklist)
				if snipers:
					self.snipers_signal.emit(snipers)


class HomeWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(config.UI_PATH, self)
		self.ui_basic_config()
		self.run_daemon()
		self.show()


	def ui_basic_config(self):
		self.setWindowIcon(QIcon(config.ICON_PATH))
		self.action_about.triggered.connect(self.show_about)


	def run_daemon(self):
		# QThread object to run daemon subprocess.
		self.thread = QThread()
		self.daemon = Daemon()
		# Move daemon to the thread.
		self.daemon.moveToThread(self.thread)
		# Connect signals and slots.
		self.thread.started.connect(self.daemon.run)
		self.daemon.blacklist_signal.connect(self.fill_blacklist)
		self.daemon.players_list_signal.connect(self.fill_players_list)
		self.daemon.snipers_signal.connect(self.fill_snipers)
		self.thread.start()


	def fill_players_list(self, players_list):
		self.clear_players_lists()
		logger.info("Llenando la lista con los nuevos jugadores.")
		for player in players_list:
			self.current_game_players_list.addItem(player)


	def fill_blacklist(self, blacklist):
		logger.info("Llenando la blacklist.")
		logger.debug(blacklist)
		for item in blacklist:
			self.blacklist_list.addItem(item)


	def fill_snipers(self, data):
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


	def clear_players_lists(self):
		logger.info("Limpiando lista anterior de jugadores.")
		self.current_game_players_list.clear()
		self.suspects_list.clear()


	def show_about(self):
		msg_box = QMessageBox()
		msg_box.setWindowTitle("Acerca de")
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setText(config.ABOUT_STRING)
		msg_box.setFixedSize(500, 500)
		msg_box.exec_()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	home = HomeWindow()
	app.exec_()