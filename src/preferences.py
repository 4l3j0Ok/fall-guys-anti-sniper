from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from static.preferences_ui import Ui_PreferencesWidget
import utils
from logger import logger


class PreferencesWindow(QWidget, Ui_PreferencesWidget):
	def __init__(self):
		try:
			super().__init__()
			self.setupUi(self)
			self.windowIcon = QIcon(":/static/icon.png")
			self.setWindowIcon(self.windowIcon)
			self.play_sound_check_box.setChecked(utils.get_data().get("preferences", {}).get("audio_checked", False))
			self.select_file_button.setEnabled(utils.get_data().get("preferences", {}).get("audio_checked", False))
			self.actual_file.setText(utils.get_data().get("preferences", {}).get("audio_file_name", "Ninguno"))
			self.select_file_button.clicked.connect(self.select_audio_file)
			self.play_sound_check_box.stateChanged.connect(self.audio_check_box_change_action)
		except Exception as ex:
			logger.exception(ex)


	def audio_check_box_change_action(self, state):
		data = utils.get_data()
		data["preferences"] = data.get("preferences", {})
		if state == Qt.Checked:
			self.select_file_button.setEnabled(True)
			data["preferences"]["audio_checked"] = True
		else:
			self.select_file_button.setEnabled(False)
			data["preferences"]["audio_checked"] = False
		utils.save_data(data)
		return


	def select_audio_file(self):
		audio_file_path = QFileDialog.getOpenFileName(
			self,
			caption = "Seleccionar archivo de audio",
			filter = "Archivo de audio WAV (*.wav)"
			)[0]
		if not audio_file_path:
			return
		audio_file_name = audio_file_path.split("/")[-1]
		data = utils.get_data()
		data["preferences"] = data.get("preferences", {})
		data["preferences"]["audio_file_path"] = audio_file_path
		data["preferences"]["audio_file_name"] = audio_file_name
		success = utils.save_data(data)
		self.actual_file.setText(audio_file_name)
		self.show_file_result(success)


	def show_file_result(self, success):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("Importar sonido")
		msg_box.setIcon(QMessageBox.Information)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setText("¡Sonido importado con éxito!")
		msg_box.setInformativeText("Este sonido sonará cada vez que se encuentre un sniper en la partida.")
		if not success:
			msg_box.setIcon(QMessageBox.Critical)
			msg_box.setText("Hubo un error al importar el archivo")
			msg_box.setInformativeText("")
		msg_box.exec_()
