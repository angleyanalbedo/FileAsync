from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QSystemTrayIcon, QMenu
from sync import sync_local
from ftp_sync import sync_ftp
from sftp_sync import sync_sftp
from webdav_sync import sync_webdav

class FileSyncApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tasks = []
        self.create_tray_icon()

    def initUI(self):
        self.setWindowTitle("文件同步工具")
        self.setGeometry(100, 100, 800, 500)

        # Task list
        self.task_list = QtWidgets.QListWidget(self)
        self.task_list.setGeometry(20, 20, 760, 300)

        # Add task button
        self.add_task_button = QtWidgets.QPushButton(self)
        self.add_task_button.setText("添加任务")
        self.add_task_button.setGeometry(20, 350, 100, 30)
        self.add_task_button.clicked.connect(self.add_task)

        # Execute tasks button
        self.execute_tasks_button = QtWidgets.QPushButton(self)
        self.execute_tasks_button.setText("执行任务")
        self.execute_tasks_button.setGeometry(140, 350, 100, 30)
        self.execute_tasks_button.clicked.connect(self.execute_tasks)

    def create_tray_icon(self):
        # System tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("icon.png"))  # 设置托盘图标
        self.tray_icon.setToolTip("文件同步工具")

        # Tray icon menu
        tray_menu = QMenu()
        restore_action = tray_menu.addAction("恢复")
        restore_action.triggered.connect(self.show_normal)
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        self.tray_icon.setContextMenu(tray_menu)

        # Double click to restore
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()

    def closeEvent(self, event):
        if self.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "文件同步工具",
                "应用程序已最小化到托盘。要退出，请使用托盘菜单。",
                QSystemTrayIcon.Information,
                2000
            )

    def add_task(self):
        task_dialog = TaskDialog(self)
        if task_dialog.exec_() == QtWidgets.QDialog.Accepted:
            task = task_dialog.get_task()
            self.tasks.append(task)
            self.task_list.addItem(f"源: {task['source']} -> 目标: {task['target']} (协议: {task['protocol']})")

    def execute_tasks(self):
        for task in self.tasks:
            source_dir = task['source']
            target_dir = task['target']
            protocol = task['protocol']
            username = task['username']
            password = task['password']
            server = task['server']

            if protocol == "Local":
                sync_local(source_dir, target_dir)
            elif protocol == "FTP":
                sync_ftp(source_dir, target_dir, server, username, password)
            elif protocol == "SFTP":
                sync_sftp(source_dir, target_dir, server, username, password)
            elif protocol == "WebDAV":
                sync_webdav(source_dir, target_dir, server, username, password)
            else:
                QMessageBox.critical(self, "错误", "不支持的协议")

        QMessageBox.information(self, "完成", "所有任务已完成")

class TaskDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TaskDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("添加任务")
        self.setGeometry(100, 100, 500, 300)

        self.source_label = QtWidgets.QLabel(self)
        self.source_label.setText("源目录:")
        self.source_label.setGeometry(20, 20, 60, 30)

        self.source_entry = QtWidgets.QLineEdit(self)
        self.source_entry.setGeometry(80, 20, 300, 30)

        self.source_button = QtWidgets.QPushButton(self)
        self.source_button.setText("选择")
        self.source_button.setGeometry(400, 20, 60, 30)
        self.source_button.clicked.connect(self.select_source_dir)

        self.target_label = QtWidgets.QLabel(self)
        self.target_label.setText("目标目录:")
        self.target_label.setGeometry(20, 60, 60, 30)

        self.target_entry = QtWidgets.QLineEdit(self)
        self.target_entry.setGeometry(80, 60, 300, 30)

        self.target_button = QtWidgets.QPushButton(self)
        self.target_button.setText("选择")
        self.target_button.setGeometry(400, 60, 60, 30)
        self.target_button.clicked.connect(self.select_target_dir)

        self.protocol_label = QtWidgets.QLabel(self)
        self.protocol_label.setText("协议:")
        self.protocol_label.setGeometry(20, 100, 60, 30)

        self.protocol_combo = QtWidgets.QComboBox(self)
        self.protocol_combo.setGeometry(80, 100, 150, 30)
        self.protocol_combo.addItems(["Local", "FTP", "SFTP", "WebDAV"])

        self.credentials_label = QtWidgets.QLabel(self)
        self.credentials_label.setText("凭证:")
        self.credentials_label.setGeometry(20, 140, 60, 30)

        self.username_entry = QtWidgets.QLineEdit(self)
        self.username_entry.setPlaceholderText("用户名")
        self.username_entry.setGeometry(80, 140, 150, 30)

        self.password_entry = QtWidgets.QLineEdit(self)
        self.password_entry.setPlaceholderText("密码")
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_entry.setGeometry(240, 140, 150, 30)

        self.server_entry = QtWidgets.QLineEdit(self)
        self.server_entry.setPlaceholderText("服务器地址")
        self.server_entry.setGeometry(80, 180, 300, 30)

        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setText("添加")
        self.add_button.setGeometry(200, 230, 100, 30)
        self.add_button.clicked.connect(self.accept)

    def select_source_dir(self):
        self.source_dir = QFileDialog.getExistingDirectory(self, "选择源目录")
        self.source_entry.setText(self.source_dir)

    def select_target_dir(self):
        self.target_dir = QFileDialog.getExistingDirectory(self, "选择目标目录")
        self.target_entry.setText(self.target_dir)

    def get_task(self):
        return {
            'source': self.source_entry.text(),
            'target': self.target_entry.text(),
            'protocol': self.protocol_combo.currentText(),
            'username': self.username_entry.text(),
            'password': self.password_entry.text(),
            'server': self.server_entry.text()
        }