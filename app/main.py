import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from app.interface import Interface
from core.notas import Notas
from app.loading import Loading
from app.windows import LoginWindow
from core.getnotes import getNotes
from multiprocessing import Process, Queue
from config.user_pass import user_pass
import os


def run_do(queue, username, password):
    try:
        from core.getFile import do 
        data_raw = do(username, password)
        queue.put({'success': True, 'data': data_raw})
    except Exception as err:
        queue.put({'success': False, 'error': str(err)})

def main():
    app = QApplication(sys.argv)
    
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/icon.png'))
    print(icon_path)
    app.setWindowIcon(QIcon(icon_path))

    login_window = LoginWindow()
    login_window.show()

    def on_login():
        option = login_window.login_result
        if not option:
            sys.exit()

        if isinstance(option, str):
            if option in user_pass.user_pass:
                username = option
                password = user_pass.user_pass[option]
            else:
                print("Usuario no reconocido")
                sys.exit()
        elif isinstance(option, list) and len(option) == 2:
            username, password = option
        else:
            print("Credenciales inválidas")
            sys.exit()

        login_window.close()

        loading = Loading()
        loading.show()
        queue = Queue()
        process = Process(target=run_do, args=(queue, username, password))
        process.start()
        error_window = None 

        def check_result():
            nonlocal error_window 
            if not queue.empty():
                result = queue.get()
                process.join()
                loading.close()

                if result.get('success'):
                    data_raw = result['data']
                    datos = getNotes(data_raw)
                    notas_obj = Notas(datos)

                    interfaz = Interface(notas_obj)
                    interfaz.showMaximized()
                else:
                    from app.windows import ErrorWindow
                    error_window = ErrorWindow()
                    error_window.getError(result['error'])
                    error_window.show()
            else:
                QTimer.singleShot(100, check_result)

        QTimer.singleShot(100, check_result)

    login_window.login_button.clicked.connect(on_login)

    sys.exit(app.exec())
