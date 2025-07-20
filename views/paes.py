from PySide6.QtWidgets import (
     QWidget, QVBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from core.calcPaes import Paes
from assets.styles.paes_styles import styles

class PaesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Calculadora de Puntaje Ponderado")
        self.setStyleSheet(styles)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.nem_input = QLineEdit()
        self.ranking_input = QLineEdit()
        self.lectura_input = QLineEdit()
        self.m1_input = QLineEdit()
        self.m2_input = QLineEdit()
        self.historia_ciencias_input = QLineEdit()

        form_layout.addRow("Puntaje NEM:", self.nem_input)
        form_layout.addRow("Puntaje Ranking:", self.ranking_input)
        form_layout.addRow("PAES Comprensión Lectora:", self.lectura_input)
        form_layout.addRow("PAES Competencia Matemática M1:", self.m1_input)
        form_layout.addRow("PAES Competencia Matemática M2:", self.m2_input)
        form_layout.addRow("PAES Historia o Ciencias:", self.historia_ciencias_input)

        self.calculate_button = QPushButton("Calcular Puntaje")
        self.calculate_button.clicked.connect(self.calculate_score)

        self.result_label = QLabel("Tu puntaje ponderado es: ")

        layout.addLayout(form_layout)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate_score(self):
        try:
            nem = float(self.nem_input.text())
            ranking = float(self.ranking_input.text())
            lectura = float(self.lectura_input.text())
            m1 = float(self.m1_input.text())
            m2 = float(self.m2_input.text())
            historia_ciencias = float(self.historia_ciencias_input.text())

            puntaje = Paes().calcScore(nem, ranking, lectura, m1, m2, historia_ciencias)
            self.result_label.setText(f"Tu puntaje ponderado es: {puntaje:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos.")
