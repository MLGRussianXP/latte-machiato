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
        self.tableUpdate()
        self.pushButton.clicked.connect(self.addEditCoffee)

    def tableUpdate(self):
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

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.resizeColumnsToContents()

    def addEditCoffee(self):
        widget = addEditCoffeeWidget(self)
        widget.show()

    def closeEvent(self, event):
        self.connection.close()


class addEditCoffeeWidget(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        # self.setupUi(self)

        self.radioButton.toggled.connect(self.radio_changed)
        self.spinBox_3.valueChanged.connect(self.id_changed)
        self.pushButton.clicked.connect(self.updateCoffee)

    def radio_changed(self, state):
        if not state:
            return self.spinBox_3.setEnabled(True)
        self.spinBox_3.setEnabled(False)

    def id_changed(self, new_id):
        cur = self.parent().connection.cursor()
        res = cur.execute("""
            SELECT * FROM coffee WHERE id = ?
        """, (new_id, )).fetchone()

        if res:
            coffee_sort = cur.execute("""
                SELECT name FROM frying WHERE id = ?
            """, (res[2],)).fetchone()[0]

            self.lineEdit.setText(res[1])
            self.comboBox.setCurrentText(coffee_sort)
            self.comboBox.setCurrentText("Молотый" if res[3] == 'True' else "В зёрнах")
            self.lineEdit_2.setText(res[4])
            self.spinBox.setValue(res[5])
            self.spinBox_2.setValue(res[6])
        else:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.spinBox.setValue(0)
            self.spinBox_2.setValue(0)

    def updateCoffee(self):
        cur = self.parent().connection.cursor()

        frying = cur.execute("""
            SELECT id FROM frying
            WHERE name = ?
        """, (self.comboBox.currentText(), )).fetchone()[0]
        coffee_type = True if self.comboBox_2.currentText() == "Молотый" else False

        if self.radioButton.isChecked():
            cur.execute("""
                INSERT INTO coffee (variety, frying, type, description, price, size)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.lineEdit.text(),
                frying,
                coffee_type,
                self.lineEdit_2.text(),
                self.spinBox.value(),
                self.spinBox_2.value()
            ))
        else:
            cur.execute("""
                UPDATE coffee
                SET variety = ?, frying = ?, type = ?, description = ?, price = ?, size = ?
                WHERE id = ?
            """, (
                self.lineEdit.text(),
                frying,
                coffee_type,
                self.lineEdit_2.text(),
                self.spinBox.value(),
                self.spinBox_2.value(),
                self.spinBox_3.value()
            ))

        self.parent().connection.commit()
        self.parent().tableUpdate()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
