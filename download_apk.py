from qtawesome import icon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QMainWindow, QPushButton,
                             QVBoxLayout, QLineEdit, QProgressBar, QComboBox,
                             QWidget, QMessageBox, QDesktopWidget,
                             QHBoxLayout, QLabel, QRadioButton)

from apk_utils import *


class DownloadAPK(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status = QLabel()
        self.text = QLineEdit(returnPressed=lambda: self.search_apk(self.text.text()))
        self.cb = QComboBox()
        self.progress = QProgressBar()
        self.init_ui()
        self.data = {}

    def init_ui(self):
        dark_blue = QRadioButton(text="Dark Blue", clicked=self.apply_dark_blue)
        dark_orange = QRadioButton("Dark Orange", clicked=self.apply_dark_orange)
        default = QRadioButton("Default", clicked=self.apply_default)
        default.setChecked(True)
        theme = QHBoxLayout()
        theme.addWidget(default)
        theme.addWidget(dark_blue)
        theme.addWidget(dark_orange)
        self.status.setObjectName("status")
        btn_start_download = QPushButton(icon('fa5s.download', color='green'), "Start downloading",
                                         clicked=lambda: self.download())
        btn_start_download.setIconSize(QSize(16, 20))
        self.text.setPlaceholderText("Enter package name then press enter")
        h_box = QHBoxLayout()
        h_box.addWidget(self.text)
        h_box.setSpacing(4)
        vb_layout = QVBoxLayout()
        vb_layout.setSpacing(8)
        vb_layout.addLayout(theme)
        vb_layout.addWidget(self.status)
        vb_layout.addLayout(h_box)
        vb_layout.addWidget(self.cb)
        vb_layout.addWidget(self.progress)
        vb_layout.addWidget(btn_start_download)
        widget = QWidget()
        widget.setLayout(vb_layout)
        self.setCentralWidget(widget)
        self.center()

    def apply_dark_orange(self):
        self.setStyleSheet(orange)

    def apply_default(self):
        self.setStyleSheet("")

    def apply_dark_blue(self):
        self.setStyleSheet(blue)
    def search_apk(self, pkg):
        self.cb.clear()
        self.status.setText("Please wait ...")
        self.status.setStyleSheet('QLabel#status {color: green}')
        link, apk_name = searching(pkg)
        if link != "" and apk_name != "":
            self.data = links_versions(link, apk_name)
            if self.data is not None:
                self.cb.addItems(list(self.data.keys()))
                self.status.setText("Pick a version and hit download")
            else:
                self.status.setStyleSheet('QLabel#status {color: red}')
                self.status.setText("No result")
        else:

            self.status.setStyleSheet('QLabel#status {color: red}')
            self.status.setText("No result")

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def download(self, path="./downloaded/"):
        print(self.text.text())
        tar = self.data[self.cb.itemText(self.cb.currentIndex())]
        if tar is not None:
            response = requests.get(tar, stream=True)
            size = int(response.headers["content-length"])

            app_size = size / (1024 * 1024)
            print(f"file size : {app_size:.2f} M")
            with open(path + self.text.text() + "_" + tar.split("/")[-1].split("-")[-3] + '.apk',
                      'wb') as apk_file:
                i = 0
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        apk_file.write(chunk)
                        i += 1024
                        value = f"downloaded {int((i / size) * 100)}%"
                        print(value)
                        self.progress.setValue((i / size) * 100)
                        QApplication.processEvents()

                QMessageBox.information(self, "Download completed", "Download finish")
        else:
            print(tar)

    def test(self):
        print(self.data[self.cb.itemText(self.cb.currentIndex())])
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication([])
    win = DownloadAPK()
    win.setWindowTitle("Download APK")
    win.setWindowIcon(icon('fa5b.android', color='#00ff00'))
    win.show()
    app.exec_()
