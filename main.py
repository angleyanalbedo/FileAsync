from PyQt5.QtWidgets import QApplication
from fileasync.gui import FileSyncApp

if __name__ == "__main__":
    app = QApplication([])
    window = FileSyncApp()
    window.show()
    app.exec_()