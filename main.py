from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtWidgets import QFileDialog

import sys

from func import func


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stocks')
        self.data = list()
        self.main_layer = QVBoxLayout(self)

        # self.dir = QFileDialog.getExistingDirectory(self, 'Open the directory', '')

        self.get_file_name = QPushButton(self)
        self.get_file_name.setText('Get the .xlsx-file')
        self.get_file_name.clicked.connect(self.getting_book)

        self.get_dir_btn = QPushButton(self)
        self.get_dir_btn.setText('Select the directory')
        self.get_dir_btn.clicked.connect(self.getting_save_dir)

        self.file_nme = QLabel(self)
        self.file_nme.setText('Select the name you want to use')
        self.inp_nme = QLineEdit(self)

        self.create = QPushButton(self)
        self.create.setText('Create the .db-file')
        self.create.setEnabled(False)
        self.create.clicked.connect(self.create_table)

        self.main_layer.addWidget(self.get_file_name)
        self.main_layer.addWidget(self.get_dir_btn)
        self.main_layer.addWidget(self.file_nme)
        self.main_layer.addWidget(self.inp_nme)
        self.main_layer.addWidget(self.create)

    def getting_book(self):
        book = QFileDialog.getOpenFileName(self, 'Select the .xlsx-file', 'C:', 'Книга (*.xlsx)')[0]
        print(book)
        self.data.append([book, 1])
        if self.check_and_format():
            self.load_button.setEnabled(True)
            self.create.setEnabled(True)

    def getting_save_dir(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select the directory', 'C:')
        print(directory)
        self.data.append([directory, 2])
        if self.check_and_format():
            self.create.setEnabled(True)

    def check_and_format(self):
        self.data = sorted(self.data, key=lambda x: x[1])
        return True if len(self.data) == 2 else False

    def create_table(self):
        if self.check_and_format():
            if self.inp_nme.text() != '':
                func(self.data[0][0], self.data[1][0], self, file_name=self.inp_nme.text())
            else:
                func(self.data[0][0], self.data[1][0], self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
