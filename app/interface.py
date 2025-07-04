import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QPushButton    
from PySide6.QtGui import QGuiApplication 
from app.windows import (AddNotaWindow, ConvertirPuntajeNotaWindow, GenerarEscalaNotasWindow, 
                     CalcularPromedioAsignaturaWindow, CalcularPromedioFinalWindow, CalcularNotaNecesariaWindow)
from app.styles import styles

class Interface(QtWidgets.QWidget):
    def __init__(self, notas_obj):  # ahora recibe el objeto Notas
        super().__init__()
        self.notas = notas_obj       # guardamos para usar
        self.setWindowTitle("School Notes")
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        self.resize(screen_size.width(), screen_size.height())
        self.setStyleSheet(styles)
        self.build_ui()

    def build_ui(self):
        menu_label = QLabel("Menu", alignment=QtCore.Qt.AlignCenter)
        menu_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")

        self.menu_layout = QVBoxLayout()
        self.menu_layout.setSpacing(12)
        self.menu_layout.addWidget(menu_label)

        self.button_map = {
            'Add Note': AddNotaWindow,
            'Convert Score to Grade': ConvertirPuntajeNotaWindow,
            'Generate Grade Scale': GenerarEscalaNotasWindow,
            'Calculate Average (Subject)': CalcularPromedioAsignaturaWindow,
            'Calculate Final Average': CalcularPromedioFinalWindow,
            'Calculate Required Grade': CalcularNotaNecesariaWindow,
        }

        for label, constructor in self.button_map.items():
            button = QPushButton(label)
            button.clicked.connect(lambda checked, c=constructor, l=label: self.open_window(c, l))
            self.menu_layout.addWidget(button)

        self.menu_layout.addStretch(1)

        menu_widget = QtWidgets.QWidget()
        menu_widget.setLayout(self.menu_layout)
        menu_widget.setFixedWidth(220)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Subject", "Type", "Weight", "Grades"])
        self.table.horizontalHeader().setStretchLastSection(True)
        for i in range(4):  # hay 4 columnas, no 5
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.populate_table()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.active_windows = []

    def open_window(self, constructor, label):
        if label == "Add Note":
            new_window = constructor(main_window=self)
        else:
            new_window = constructor(parent=None)
        self.active_windows.append(new_window)
        new_window.show()

    def populate_table(self):
        rows = []
        # Suponiendo que self.notas tiene un atributo o método para obtener datos como el df anterior
        # Por ejemplo, si en Notas está guardado el diccionario en self.data
        df = getattr(self.notas, 'data', {})  # O cambia 'data' por el atributo correcto
        for subject, types in df.items():
            for eval_type, content in types.items():
                row = (
                    subject,
                    eval_type,
                    str(content.get("ponderacion", "")),
                    ", ".join(str(n) for n in content.get("notas", []))
                )
                rows.append(row)

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(i, j, item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Para prueba, si quieres un df dummy
    dummy_data = {
        "Math": {
            "tests": {"ponderacion": 40, "notas": [5, 6, 7]},
            "homeworks": {"ponderacion": 60, "notas": [8, 9]}
        }
    }
    class DummyNotas:
        def __init__(self, data):
            self.data = data
    widget = Interface(DummyNotas(dummy_data))
    widget.show()
    sys.exit(app.exec())
