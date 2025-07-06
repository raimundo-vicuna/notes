import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QProgressBar,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtGui import QIcon


class Loading(QDialog):
     def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("School Notes")
        
        lado = 200
        self.setFixedSize(lado, lado)
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel('Loading...', alignment=QtCore.Qt.AlignCenter)
  
        self.spinner = QProgressBar()      
        self.spinner.setRange(0, 0)
        self.spinner.setTextVisible(False)
        self.spinner.setFixedWidth(180)
        
        layout.addWidget(self.label)
        layout.addWidget(self.spinner)
        self.setLayout(layout)
