from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox

class msgBox(QObject):
	def info(self, title="", inf_text="", text=""):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		msg_box.exec_()

	def warning(self, title="", inf_text="", text=""):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Warning)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		msg_box.exec_()

	def error(self, title="", inf_text="", text=""):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		msg_box.exec_()

	def question(self, title="", inf_text="", text=""):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		msg_box.exec_()

	def info_result(self, title="", inf_text="", text="", yes = "Sí", no = "No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Warning)
		button_yes = msg_box.button(QMessageBox.Yes)
		button_no = msg_box.button(QMessageBox.No)
		button_yes.setText(yes)
		button_no.setText(no)
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		result = msg_box.exec()
		if result == QMessageBox.Yes:
			return True
		return False

	def warning_result(self, title="", inf_text="", text="", yes = "Sí", no = "No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		button_yes = msg_box.button(QMessageBox.Yes)
		button_no = msg_box.button(QMessageBox.No)
		button_yes.setText(yes)
		button_no.setText(no)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		result = msg_box.exec()
		if result == QMessageBox.Yes:
			return True
		return False

	def error_result(self, title="", inf_text="", text="", yes = "Sí", no = "No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Warning)
		button_yes = msg_box.button(QMessageBox.Yes)
		button_no = msg_box.button(QMessageBox.No)
		button_yes.setText(yes)
		button_no.setText(no)
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		result = msg_box.exec()
		if result == QMessageBox.Yes:
			return True
		return False
