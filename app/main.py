import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from multiprocessing import Process, Queue
import os

from app.windows import LoginWindow
from config.user_pass import user_pass
from core.getFile import do  # tu función para login con Selenium
from core.getnotes import getNotes
from core.notas import Notas
from app.interface import Interface
from app.loading import Loading

def run_do(queue, username, password):
    try:
        data_raw = do(username, password)
        queue.put({'success': True, 'data': data_raw})
    except Exception as err:
        queue.put({'success': False, 'error': str(err)})

def main():
    app = QApplication(sys.argv)
    
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/icon.png'))
    app.setWindowIcon(QIcon(icon_path))

    login_window = LoginWindow()
    login_window.show()
    app.exec()  # Para que la ventana se muestre y cierre correctamente

    option = login_window.login_result
    if not option:
        sys.exit()

    if isinstance(option, str):  # Usuario predefinido
        if option in user_pass.user_pass:
            user_info = user_pass.user_pass[option]
            username = list(user_info.keys())[0]
            password = user_info[username]
        else:
            print("Usuario no reconocido")
            sys.exit()

    elif isinstance(option, list) and len(option) == 2:  # Nuevo usuario
        username, password = option
    else:
        print("Credenciales inválidas")
        sys.exit()

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

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
