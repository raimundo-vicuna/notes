import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QComboBox
from windows import (
    AddNotaWindow,
    ConvertirPuntajeNotaWindow,
    GenerarEscalaNotasWindow,
    CalcularPromedioAsignaturaWindow,
    CalcularPromedioFinalWindow,
    CalcularNotaNecesariaWindow
)

class interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Choice an option", alignment=QtCore.Qt.AlignCenter)
        
        self.comboBox = QComboBox(self)
        self.comboBox.addItem('Default')
        self.comboBox.addItem('Añadir Nota')
        self.comboBox.addItem('Convertir Puntaje A Nota')
        self.comboBox.addItem('Generar Escala De Notas')
        self.comboBox.addItem('Calcular Promedio(asignatura)')
        self.comboBox.addItem('Calcular Promedio Final')
        self.comboBox.addItem('Calcular Nota Necesaria')
        self.comboBox.setFixedWidth(250) 
        
        self.button = QtWidgets.QPushButton("next")
        self.button.setFixedWidth(100) 
        self.button.clicked.connect(self.next_step)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.text, alignment=QtCore.Qt.AlignCenter) 
        self.layout.addWidget(self.comboBox, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
    
        self.window_map = {
            'Añadir Nota': AddNotaWindow,
            'Convertir Puntaje A Nota': ConvertirPuntajeNotaWindow,
            'Generar Escala De Notas': GenerarEscalaNotasWindow,
            'Calcular Promedio(asignatura)': CalcularPromedioAsignaturaWindow,
            'Calcular Promedio Final': CalcularPromedioFinalWindow,
            'Calcular Nota Necesaria': CalcularNotaNecesariaWindow,
        }
        
        self.active_windows = []
    
    def get_option(self):
        return self.comboBox.currentText()
    
    def next_step(self):
        selected_option = self.get_option()
        self.text.setText(f"Continues in: {selected_option}")

        if selected_option in self.window_map:
            WindowConstructor = self.window_map[selected_option]
            new_window = WindowConstructor(parent=None) 
            self.active_windows.append(new_window)
            new_window.show()
        elif selected_option == 'Default':
            pass
        else:
            self.text.setText("Error: Opción no reconocida.")
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 

    widget = interface()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())