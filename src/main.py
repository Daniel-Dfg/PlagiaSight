"""
    Coders: Daniel-Dfg and Luckyyyin
"""
from sys import argv
from PySide6.QtWidgets import QApplication
from UI_Functional.main_window import MainWindow
from time import time
CURRENT_TIME = None

if __name__ == "__main__":
    CURRENT_TIME = time()
    # Check whether there is already a running QApplication (e.g., if running from an IDE).
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(argv)

    window = MainWindow()
    window.show()
    window.raise_()
    print(f"Startup time: {time()-CURRENT_TIME}")
    qapp.exec()
