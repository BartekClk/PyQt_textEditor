from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal

class QLabel_Clickable(QLabel):
    clicked=pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()