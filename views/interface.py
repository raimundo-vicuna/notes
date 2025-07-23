from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QGuiApplication, QIcon
from views.windows import (AddNotaWindow, ConvertirPuntajeNotaWindow, GenerarEscalaNotasWindow, CalcularNotaNecesariaWindow)
from views.graphs import DataAnalysisWindow
from assets.styles.styles import styles
from PySide6.QtCore import Qt
from views.paes import PaesWindow
from views.classmates import ClassmatesWindow

class Interface(QtWidgets.QWidget):
    def __init__(self, notas_obj, classmates): 
        super().__init__()
        self.notas = notas_obj
        self.classmates = classmates
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
        'Add Note': lambda: AddNotaWindow(self.notas, main_window=self),
        'Convert Score to Grade': lambda: ConvertirPuntajeNotaWindow(self.notas),
        'Generate Grade Scale': lambda: GenerarEscalaNotasWindow(self.notas),
        'Calculate Required Grade': lambda: CalcularNotaNecesariaWindow(self.notas),
        'Get data analysis': lambda: DataAnalysisWindow(self.notas),
        'Paes': PaesWindow,
        'Classmates': lambda: ClassmatesWindow(self.classmates),
        }


        for label, constructor in self.button_map.items():
            if label == 'Add Note':
                row_layout = QHBoxLayout()

                button = QPushButton(label)
                button.clicked.connect(lambda checked, c=constructor, l=label: self.open_window(c, l))

                delete_button = QPushButton()
                delete_icon = QIcon('assets/icons/return.png')
                delete_button.setIcon(delete_icon)
                delete_button.setToolTip("Delete Note")
                delete_button.clicked.connect()

                row_layout.addWidget(button, stretch=9)
                row_layout.addWidget(delete_button, stretch=1)

                self.menu_layout.addLayout(row_layout)

            else:
                button = QPushButton(label)
                button.clicked.connect(lambda checked, c=constructor, l=label: self.open_window(c, l))
                self.menu_layout.addWidget(button)


        self.menu_layout.addStretch(1)

        self.avr_label = QLabel("", alignment=Qt.AlignCenter)
        self.setAverage()
        self.avr_label.setAlignment(Qt.AlignCenter)
        self.avr_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.avr_label)
        bottom_layout.addStretch()

        self.menu_layout.addLayout(bottom_layout)                

        menu_widget = QtWidgets.QWidget()
        menu_widget.setLayout(self.menu_layout)
        menu_widget.setFixedWidth(220)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Subject", "Type", 'Subject Avr', "Weight", "Grades"])
        self.table.horizontalHeader().setStretchLastSection(True)
        for i in range(5):
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
        new_window = constructor()
        self.active_windows.append(new_window)
        new_window.show()

    def populate_table(self):
        rows = []
        df = getattr(self.notas, 'data', {}) 
        for subject, types in df.items():
            subject_avg = self.notas.calc_promedio(subject)
            subject_avg_str = f"{subject_avg:.1f}" if subject_avg is not None else ""

            for eval_type, content in types.items():
                row = (
                    subject,
                    eval_type,
                    subject_avg_str,
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

    
    def setAverage(self):
            self.avr_label.setText(f'Your Final Average is: {self.notas.calc_promedio_final()}')
    
    def closeEvent(self, event):
        QtWidgets.QApplication.quit()
