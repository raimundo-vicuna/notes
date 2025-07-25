from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import * 
from core.notas import Notas
types = ['Pruebas', 'Controles', 'Paes (Only Language)']

def getSubjects(notas_obj):
    return list(notas_obj.data.keys())

class AddNotaWindow(QMainWindow):
    def __init__(self, notas_obj, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window 
        self.notas_obj = notas_obj
        self.main_window = main_window
        

        self.setWindowTitle("Add Note")
        self.setGeometry(200, 200, 300, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.nota_input = QLineEdit(self)
        self.nota_input.setPlaceholderText("Note")
        self.nota_input.setFixedWidth(50)
        
        self.subject_input = QComboBox(self)
        self.subject_input.addItems(getSubjects(notas_obj))
        self.subject_input.setFixedWidth(150)
        
        self.type_input = QComboBox(self)
        self.type_input.addItems(types)
        self.type_input.setFixedWidth(90)
        
        self.label = QLabel("Add Note", alignment=Qt.AlignCenter)
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.nota_input)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.type_input)

        self.save_button = QPushButton("Save Note", self)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_note)

    def save_note(self):
        try:
            entered_note = float(self.nota_input.text().replace(",", "."))
        except ValueError:
            return 

        if entered_note > 7:
            self.label.setText('Grade cannot be greater than 7')
        
        subject = self.subject_input.currentText()
        tipo = self.type_input.currentText().split()[0].lower()

        self.notas_obj.add_nota(subject, entered_note, tipo)

        if self.main_window:
            self.main_window.populate_table()
            self.main_window.setAverage()

        self.close()

class popNoteWindow(QMainWindow):
    def __init__(self, notas_obj, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window 
        self.notas_obj = notas_obj
        self.main_window = main_window
        
        self.setWindowTitle('Remove Note')
        self.setGeometry(200, 200, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.nota_input = QLineEdit(self)
        self.nota_input.setPlaceholderText("Note")
        self.nota_input.setFixedWidth(50)
        
        self.subject_input = QComboBox(self)
        self.subject_input.addItems(getSubjects(notas_obj))
        self.subject_input.setFixedWidth(150)
        
        self.type_input = QComboBox(self)
        self.type_input.addItems(types)
        self.type_input.setFixedWidth(90)
        
        self.label = QLabel("Remove Note", alignment=Qt.AlignCenter)
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.nota_input)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.type_input)

        self.save_button = QPushButton("Save Note", self)
        layout.addWidget(self.save_button)
        
        try:
            entered_note = float(self.nota_input.text().replace(",", "."))
        except ValueError:
            return 
        
        subject = self.subject_input.currentText()
        tipo = self.type_input.currentText().split()[0].lower()

        
        self.save_button.clicked.connect(Notas.quit_note(subject, entered_note, tipo))

    


class ConvertirPuntajeNotaWindow(QMainWindow):
    def __init__(self, notas_obj, parent=None):
        super().__init__(parent)
        
        self.notas_obj = notas_obj
        
        self.setWindowTitle("Convert Score to Grade")
        self.setGeometry(200, 200, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.score = QLineEdit(self)
        self.score.setPlaceholderText("Score")
        
        self.p_max = QLineEdit(self)
        self.p_max.setPlaceholderText('Max Score')
        
        self.requirement = QLineEdit(self)
        self.requirement.setPlaceholderText('Requirement')
        self.requirement.setText('0.6')
        
        self.min_grade = QLineEdit(self)
        self.min_grade.setPlaceholderText('Min Grade')
        self.min_grade.setText('2')
        
        self.apr_grade = QLineEdit(self)
        self.apr_grade.setPlaceholderText('Approval Grade')
        self.apr_grade.setText('4')

        self.max_grade = QLineEdit(self)
        self.max_grade.setPlaceholderText('Max Grade')
        self.max_grade.setText('7')

        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addStretch(1)

        self.display_label = QLabel("Convert Score to Grade", alignment=Qt.AlignCenter)
        main_layout.addWidget(self.display_label)

        row1_layout = QHBoxLayout()
        row1_layout.addStretch(1)
        row1_layout.addWidget(self.score)
        row1_layout.addWidget(self.p_max)
        row1_layout.addStretch(1)
        main_layout.addLayout(row1_layout)

        row2_layout = QHBoxLayout()
        row2_layout.addStretch(1)
        row2_layout.addWidget(self.requirement)
        row2_layout.addWidget(self.min_grade)
        row2_layout.addStretch(1)
        main_layout.addLayout(row2_layout)
        
        row3_layout = QHBoxLayout()
        row3_layout.addStretch(1)
        row3_layout.addWidget(self.apr_grade)
        row3_layout.addWidget(self.max_grade)
        row3_layout.addStretch(1)
        main_layout.addLayout(row3_layout)

        main_layout.addStretch(1)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.show_grade)
        main_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)
        
    def get_values(self):
        inputs = [
            self.score,
            self.p_max,
            self.requirement,
            self.min_grade,
            self.apr_grade,
            self.max_grade
        ]
        
        return [float(field.text()) for field in inputs]
    
    def show_grade(self):
        try:
            calculated_grade = self.notas_obj.convertir_puntaje_a_nota(*self.get_values())
            
            self.display_label.setText(f"Grade: {calculated_grade:.1f}")
        except ValueError:
            self.display_label.setText("Invalid input. Please enter numbers.")
        except Exception as e:
            self.display_label.setText(f"Error: {e}")

class GenerarEscalaNotasWindow(QMainWindow):
    def __init__(self, notas_obj, parent=None):
        super().__init__(parent)
        
        self.notas_obj = notas_obj

        self.setWindowTitle("Generate Grade Scale")
        self.setGeometry(200, 200, 400, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.p_max = QLineEdit(self)
        self.p_max.setPlaceholderText('Max Score')
        
        self.requirement = QLineEdit(self)
        self.requirement.setPlaceholderText('Requirement')
        self.requirement.setText("0.6")
        
        self.min_grade = QLineEdit(self)
        self.min_grade.setPlaceholderText('Min Grade')
        self.min_grade.setText("2.0")
        
        self.apr_grade = QLineEdit(self)
        self.apr_grade.setPlaceholderText('Approval Grade')
        self.apr_grade.setText("4.0")

        self.max_grade = QLineEdit(self)
        self.max_grade.setPlaceholderText('Max Grade')
        self.max_grade.setText("7.0")
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addStretch(1)

        self.display_label = QLabel("Generate Grade Scale", alignment=Qt.AlignCenter)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_area_content = QWidget()
        self.scroll_area_content_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area_content_layout.addWidget(self.display_label, alignment=Qt.AlignCenter)
        self.scroll_area.setWidget(self.scroll_area_content)

        self.scroll_area.setVisible(False)

        main_layout.addWidget(self.scroll_area)

        self.input_container = QWidget(self)
        input_layout = QVBoxLayout(self.input_container)

        row1_layout = QHBoxLayout()
        row1_layout.addStretch(1)
        row1_layout.addWidget(self.p_max)
        row1_layout.addStretch(1)
        input_layout.addLayout(row1_layout)

        row2_layout = QHBoxLayout()
        row2_layout.addStretch(1)
        row2_layout.addWidget(self.requirement)
        row2_layout.addWidget(self.min_grade)
        row2_layout.addStretch(1)
        input_layout.addLayout(row2_layout)
        
        row3_layout = QHBoxLayout()
        row3_layout.addStretch(1)
        row3_layout.addWidget(self.apr_grade)
        row3_layout.addWidget(self.max_grade)
        row3_layout.addStretch(1)
        input_layout.addLayout(row3_layout)

        main_layout.addWidget(self.input_container)
        
        main_layout.addStretch(1)
        
        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.show_scale)
        main_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search score...")
        self.search_input.returnPressed.connect(self.search_score)
        self.search_input.setVisible(False)
        main_layout.addWidget(self.search_input, alignment=Qt.AlignCenter)

        self.current_scale_data = []

    def get_values(self):
        p_max_value = int(float(self.p_max.text()))
        requirement_value = float(self.requirement.text())
        min_grade_value = float(self.min_grade.text())
        apr_grade_value = float(self.apr_grade.text())
        max_grade_value = float(self.max_grade.text())
        
        return [
            p_max_value,
            requirement_value,
            min_grade_value,
            apr_grade_value,
            max_grade_value
        ]
    
    def show_scale(self):
        try:
            self.current_scale_data = self.notas_obj.generar_escala(*self.get_values())
            self.display_label.setText("\n".join(self.current_scale_data))
            
            self.input_container.setVisible(False)
            self.generate_button.setVisible(False)
            self.scroll_area.setVisible(True)
            self.search_input.setVisible(True)

        except ValueError:
            self.display_label.setText("Invalid input. Please enter numbers.")
            self.scroll_area.setVisible(True)
            self.search_input.setVisible(False)
        except Exception as e:
            self.display_label.setText(f"Error: {e}")
            self.scroll_area.setVisible(True)
            self.search_input.setVisible(False)

    def search_score(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            self.display_label.setText("\n".join(self.current_scale_data))
            return

        try:
            search_score_int = int(search_text)
            found_line = None
            search_prefix = f"{search_score_int:8} →" 

            for line in self.current_scale_data:
                if line.startswith(search_prefix):
                    found_line = line
                    break
            
            if found_line:
                self.display_label.setText(found_line)
            else:
                self.display_label.setText(f"Score '{search_score_int}' not found on the scale.")
        except ValueError:
            self.display_label.setText("Please enter a valid integer to search.")
        except Exception as e:
            self.display_label.setText(f"Error during search: {e}")

class CalcularPromedioAsignaturaWindow(QMainWindow):
    def __init__(self, notas_obj, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculate average (Subject)")
        self.setGeometry(200, 200, 300, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.notas_obj = notas_obj
        self.label = QLabel("Calculate average (Subject)", alignment=Qt.AlignCenter)
        
        self.subject = QComboBox(self)
        self.subject.addItems(getSubjects(notas_obj))
        
        self.average_button = QPushButton("Get", self)
        self.average_button.clicked.connect(self.get_subject_avr)
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.subject)
        layout.addWidget(self.average_button)
        
    def get_subject_avr(self):
        subject = self.subject.currentText()
        average = self.notas_obj.calc_promedio(subject)
        self.label.setText(f'The average of {subject} is {average}')
       
class CalcularNotaNecesariaWindow(QMainWindow):
    def __init__(self, notas_obj, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        self.notas_obj = notas_obj
        
        self.setWindowTitle("Calculate Necessary Note")
        self.setGeometry(200, 200, 300, 250)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        self.label = QLabel("Calculate Necessary Note", alignment=Qt.AlignCenter) 
        main_layout.addWidget(self.label)
        
        self.subject = QComboBox(self)
        self.subject.addItems(getSubjects(notas_obj))
        
        self.type_input = QComboBox(self)
        self.type_input.addItems(types)
        self.arg_expected = QLineEdit(self)
        self.arg_expected.setPlaceholderText('Expected Average')
        
        main_layout.addWidget(self.subject)
        main_layout.addWidget(self.type_input)
        main_layout.addWidget(self.arg_expected)
        
        self.get_button = QPushButton('Get', self)
        self.get_button.clicked.connect(self.get_expected_avr) 
        main_layout.addWidget(self.get_button)
        
    def get_expected_avr(self):
            expected_avg_str = self.arg_expected.text().strip()
            if not expected_avg_str:
                self.label.setText("Please enter an expected average.")
                return
            expected_a = float(expected_avg_str)
            subject = self.subject.currentText()
            type_note = self.type_input.currentText().lower()
            necessary_note = self.notas_obj.nota_necesaria(expected_a, subject, type_note)
            self.label.setText(f"Necessary Note: {necessary_note}")

class ErrorWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        self.setGeometry(200, 200, 300, 250)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        self.label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label)
        
        self.closeButton = QPushButton('Close')
        self.closeButton.clicked.connect(QApplication.quit)
        main_layout.addWidget(self.closeButton) 
        
    def getError(self, err):
        self.label.setText('An error occurred, please try again.\n' + str(err))
        self.label.show()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 300, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        content_layout.setAlignment(Qt.AlignVCenter)

        combo_row = QHBoxLayout()
        
#-------------- Change this part when developing the db-----------------#
        from config.user_pass import user_pass
        users = list(user_pass.user_pass.keys()) + ['New User', 'Choose an option']
#-----------------------------------------------------------------------#

        user_col = QVBoxLayout()
        user_label = QLabel("Usuario")
        self.combo = QComboBox()
        self.combo.addItems(users[::-1])
        self.combo.currentTextChanged.connect(self.check_new_user)
        user_col.addWidget(user_label)
        user_col.addWidget(self.combo)
        combo_row.addLayout(user_col, 4)

        period_col = QVBoxLayout()
        period_label = QLabel("Period")
        self.period_combo = QComboBox()
        self.period_combo.addItems([str(p) for p in ['Choose an option', 1, 2, '1+2']])
        
        period_col.addWidget(period_label)
        period_col.addWidget(self.period_combo)
        combo_row.addLayout(period_col, 1)

        content_layout.addLayout(combo_row)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.name_input.setVisible(False)
        content_layout.addWidget(self.name_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Usuario")
        self.password_input.setVisible(False)
        content_layout.addWidget(self.password_input)
        
        self.save_checkbox = QCheckBox('Save')
        self.save_checkbox.setVisible(False)
        content_layout.addWidget(self.save_checkbox)
        self.save_checkbox.clicked.connect(self.save_user)
        
        self.name_input.textChanged.connect(self.update_login_state)
        self.password_input.textChanged.connect(self.update_login_state)

        main_layout.addStretch()
        main_layout.addLayout(content_layout)
        main_layout.addStretch()

        self.login_button = QPushButton("Login")
        main_layout.addWidget(self.login_button, alignment=Qt.AlignBottom)
        self.login_button.clicked.connect(self.login_clicked)

        self.login_result = None

        self.combo.currentIndexChanged.connect(self.update_login_state)
        self.period_combo.currentIndexChanged.connect(self.update_login_state)
        self.update_login_state()

    def update_login_state(self):
        user_text = self.combo.currentText()
        period_text = self.period_combo.currentText()

        is_user_selected = user_text != "Choose an option"
        is_period_selected = period_text != "Choose an option"

        if user_text == "New User":
            name_filled = bool(self.name_input.text())
            password_filled = bool(self.password_input.text())
            self.login_button.setEnabled(is_period_selected and name_filled and password_filled)
        else:
            self.login_button.setEnabled(is_user_selected and is_period_selected)

    def check_new_user(self, text):
        is_new = text == "New User"
        self.name_input.setVisible(is_new)
        self.password_input.setVisible(is_new)
        self.save_checkbox.setVisible(is_new)
    
    def save_user():
        pass
        #add logic when developing the database

    def go(self):
#-------------- Change this part when developing the db-----------------#
        user = self.combo.currentText()
        if user != 'New User':
            return user
#-----------------------------------------------------------------------#
        else:
            username = self.name_input.text()
            password = self.password_input.text()
            period = self.period_combo.currentText()
            return [username, password, period]

    def login_clicked(self):
        self.login_result = self.go()
        self.close()