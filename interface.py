import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QLabel,
    QVBoxLayout, QHBoxLayout, QPushButton
)   
from PySide6.QtGui import QGuiApplication 
from windows import (
    AddNotaWindow,
    ConvertirPuntajeNotaWindow,
    GenerarEscalaNotasWindow,
    CalcularPromedioAsignaturaWindow,
    CalcularPromedioFinalWindow,
    CalcularNotaNecesariaWindow
)
from notas import df


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Notes")
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        self.resize(screen_size.width(), screen_size.height())

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #2c2c2c;
                border-radius: 6px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #2c2c2c;
            }
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c2c2c;
                border: none;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 6px;
                border: none;
            }
        """)

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
        for i in range(0,5):
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
    widget = Interface()
    widget.show()
    sys.exit(app.exec())
