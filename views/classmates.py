from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QSizePolicy, QLineEdit, QComboBox, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pandas as pd

from assets.styles.classmates_styles import styles

class ClassmatesWindow(QWidget):
    def __init__(self, classmates_obj):
        super().__init__()

        self.setWindowTitle("Classmates List")
        self.showMaximized()

        self.classmates = classmates_obj
        self.df_original = self.classmates.getAlldf()
        self.df_filtered = self.df_original.copy()

        layout = QVBoxLayout()
        
        title = QLabel("Classmates List")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        filters_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name...")
        self.search_box.textChanged.connect(self.filter_data)

        self.month_box = QComboBox()
        self.month_box.addItem("All months")
        self.month_box.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_box.currentIndexChanged.connect(self.filter_data)

        filters_layout.addWidget(self.search_box)
        filters_layout.addWidget(self.month_box)
        layout.addLayout(filters_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Birthdate", "Address"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

        self.setStyleSheet(styles)

    def load_data(self):
        df = self.df_filtered
        self.table.setRowCount(len(df))
        for row in range(len(df)):
            for col in range(3):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def filter_data(self):
        text = self.search_box.text().lower()
        month_index = self.month_box.currentIndex()

        df_filtered = self.df_original.copy()

        if text:
            df_filtered = df_filtered[df_filtered.iloc[:, 0].str.lower().str.contains(text)]

        if month_index != 0:
            month = month_index
            df_filtered = df_filtered[
                pd.to_datetime(df_filtered.iloc[:, 1], errors='coerce').dt.month == month
            ]

        self.df_filtered = df_filtered
        self.load_data()
