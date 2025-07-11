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
     def __init__(self, parent=None, period=None):
        super().__init__(parent)

        self.period = period
        
        self.setWindowTitle("School Notes")
        self.lado = 200        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinner = QProgressBar()      
        self.spinner.setRange(0, 0)
        self.spinner.setTextVisible(False)
        self.spinner_large = 180
                
        is_heavy = str(period) == '1+2'

        if is_heavy:
            self.setFixedSize(self.lado * 2, self.lado * 2)

        text = 'Loading... \n This may take longer than usual given the volume of files...' if is_heavy else 'Loading...'
        self.label = QLabel(text, alignment=QtCore.Qt.AlignCenter)

        self.spinner.setFixedWidth(self.spinner_large * (2 if is_heavy else 1))

        layout.addWidget(self.label)
        layout.addWidget(self.spinner)
        self.setLayout(layout)
