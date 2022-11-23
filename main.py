import sqlite3
import sys

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        # self.setupUi(self)

        self.connection = sqlite3.connect("coffee.sqlite")
        self.frying = {
            idx: el for idx, el in self.connection.cursor().execute("SELECT * FROM frying").fetchall()
        }
        self.tableInit()

    def tableInit(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "ID",
                "Название",
                "Степень обжарки",
                "Молотый/в зёрнах",
                "Вкус",
                "Цена",
                "Объём упаковки"
            ]
        )
        self.tableWidget.resizeColumnsToContents()

        res = self.connection.cursor().execute(f"""
            SELECT * FROM coffee
        """).fetchall()

        self.tableWidget.setRowCount(0)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                if j == 2:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(self.frying[elem]))
                elif j == 3:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem("Молотый" if elem == "True" else "В зёрнах"))
                else:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
