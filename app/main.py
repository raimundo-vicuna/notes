import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from app.interface import Interface
from core.notas import Notas
from app.loading import Loading
from core.getnotes import getNotes
from multiprocessing import Process, Queue

def run_do(queue):
    from core.getFile import do 
    data_raw = do()
    queue.put(data_raw)

def main():
    app = QApplication(sys.argv)

    loading = Loading()
    loading.show()

    queue = Queue()
    process = Process(target=run_do, args=(queue,))
    process.start()

    def check_result():
        if not queue.empty():
            data_raw = queue.get()
            datos = getNotes(data_raw)
            notas_obj = Notas(datos)

            interfaz = Interface(notas_obj)
            interfaz.show()

            loading.close()
            process.join()
        else:
            QTimer.singleShot(100, check_result)

    QTimer.singleShot(100, check_result)

    sys.exit(app.exec())

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  
    main()
