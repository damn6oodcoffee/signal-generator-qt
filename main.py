import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(Path('ct_app_style.qss').read_text())
    window = MainWindow()
    window.show()
    app.exec()
