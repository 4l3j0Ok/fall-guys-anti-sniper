import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import utils
import config
from logger import logger


#TODO Send windows notification if sniper detected https://www.youtube.com/watch?v=p1w-FZclhXs
#https://wiki.python.org/moin/PyQt/Threading,_Signals_and_Slots

class Daemon(QObject):
	blacklist_signal = pyqtSignal(list)
	players_list_signal = pyqtSignal(list)

	def run(self):
		self.blacklist_signal.emit(utils.get_blacklist())
		players_list = []
		index_list = []
		cached_line = ""
		logger.info("Buscando nueva partida...")
		while True:
			new_game, index_list, cached_line = utils.find_new_game(index_list, cached_line)
			if new_game:
				logger.info("Hay nueva partida, guardo lo previo y emito señal.")
				result_save = utils.save_previous_game_players(players_list, logger)
				logger.info("Result de save_previous_game_players: {}".format(result_save))
				players_list = utils.get_players(index_list[-1], logger)
				self.players_list_signal.emit(players_list)

class HomeWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui_components = uic.loadUi(config.UI_PATH, self)
		self.run_daemon()
		self.show()

	def run_daemon(self):
		# QThread object to run daemon subprocess.
		self.thread = QThread()
		self.daemon = Daemon()
		# Move daemon to the thread.
		self.daemon.moveToThread(self.thread)
		# Connect signals and slots
		self.thread.started.connect(self.daemon.run)
		self.daemon.blacklist_signal.connect(self.fill_blacklist)
		self.daemon.players_list_signal.connect(self.fill_players_list)
		self.thread.start()

	def fill_players_list(self, players_list):
		self.clear_players_list()
		logger.info("Llenando la lista con los nuevos jugadores.")
		for player in players_list:
			self.current_game_players_list.addItem(player)

	def clear_players_list(self):
		logger.info("Limpiando lista anterior de jugadores.")
		self.current_game_players_list.clear()

	def fill_blacklist(self, blacklist):
		logger.info("Llenando la blacklist.")
		logger.debug(blacklist)
		for item in blacklist:
			if item.get("name"):
				self.blacklist_list.addItem(item["name"])


if __name__ == "__main__":
	app = QApplication(sys.argv)
	home = HomeWindow()
	app.exec_()