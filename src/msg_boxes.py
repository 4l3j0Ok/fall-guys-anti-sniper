from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox

class MsgBox(QObject):
	def info(self, title="", inf_text="", text="", return_result = False, yes = "Sí", no="No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		if return_result:
			msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			button_yes = msg_box.button(QMessageBox.Yes)
			button_yes.setText(yes)
			button_no = msg_box.button(QMessageBox.No)
			button_no.setText(no)
		result = msg_box.exec_()
		if return_result:
			if result == QMessageBox.Yes:
				return True
			return False

	def warning(self, title="", inf_text="", text="", return_result = False, yes = "Sí", no="No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		if return_result:
			msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			button_yes = msg_box.button(QMessageBox.Yes)
			button_yes.setText(yes)
			button_no = msg_box.button(QMessageBox.No)
			button_no.setText(no)
		result = msg_box.exec_()
		if return_result:
			if result == QMessageBox.Yes:
				return True
			return False

	def error(self, title="", inf_text="", text="", return_result = False, yes = "Sí", no="No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		if return_result:
			msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			button_yes = msg_box.button(QMessageBox.Yes)
			button_yes.setText(yes)
			button_no = msg_box.button(QMessageBox.No)
			button_no.setText(no)
		result = msg_box.exec_()
		if return_result:
			if result == QMessageBox.Yes:
				return True
			return False

	def question(self, title="", inf_text="", text="", return_result = False, yes = "Sí", no="No"):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle(title)
		msg_box.setIcon(QMessageBox.Question)
		msg_box.setDefaultButton(QMessageBox.Close)
		msg_box.setInformativeText(inf_text)
		msg_box.setText(text)
		if return_result:
			msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			button_yes = msg_box.button(QMessageBox.Yes)
			button_yes.setText(yes)
			button_no = msg_box.button(QMessageBox.No)
			button_no.setText(no)
		result = msg_box.exec_()
		if return_result:
			if result == QMessageBox.Yes:
				return True
			return False
