import sys
import sqlite3
from PyQt6 import uic, QtCore, QtWidgets  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QButtonGroup, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path
import PyQt6
msg = MIMEMultipart()


def send_emails(receiver_emails, subject, body, sender_email, password):
    smtp_server = smtplib.SMTP(f"smtp.{sender_email.split('@')[1]}", 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, password)
    # Настройка параметров сообщения
    msg["From"] = sender_email
    msg["To"] = ''
    msg["Subject"] = subject

    # Добавление текста в сообщение
    msg.attach(MIMEText(body, "plain"))
    smtp_server.sendmail(sender_email, receiver_emails, msg.as_string())

    # Закрытие соединения
    smtp_server.quit()


class RegDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('regForm.ui', self)  # Загружаем дизайн
        self.addBtn.clicked.connect(self.reg)

    def reg(self):
        with open('date.txt', "w") as file:
            mail = self.mailinp.text()
            password = self.passwordinp.text()
            file.write(f"{mail}\n{password}")
        QMessageBox.information(self, " ", "Вы успешно зарегестрировались!")
        self.close()


class MailingDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('mailingForm.ui', self)  # Загружаем дизайн
        self.crtBtn.clicked.connect(self.createM)
        self.d = RegDialog()
        self.openTxt.clicked.connect(self.opnTxt)

    def createDialog(self):
        self.show()
        if not os.path.exists("date.txt"):
            self.d.show()

    def opnTxt(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберете файл', '', "Текст (*.txt)")[0]
        with open(fname, "r", encoding="utf-8") as file:
            self.body.setPlainText(file.read())

    def createM(self):
        try:
            with open('date.txt', "r") as file:
                date = file.read().split("\n")
                mail = date[0]
                password = date[1]
        except:
            QMessageBox.critical(self, " ", "Вы не зарегестрировались!")
            self.close()
        else:
            tp = self.chB.currentIndex()
            gt = self.inp.text()
            com = ""
            if tp == 0:
                if gt.isdigit():
                    com = f"""
                                    SELECT mail FROM users
                                    WHERE id = {int(gt)};
                                    """
                else:
                    QMessageBox.critical(self, " ", "Введите число")

            elif tp == 1:
                com = f"""
                                SELECT mail FROM users
                                WHERE name = "{gt}";
                                """
            elif tp == 2:
                com = f"""
                                SELECT mail FROM users
                                WHERE surname = "{gt}";
                                """
            elif tp == 3:
                com = f"""
                                SELECT mail FROM users
                                WHERE mail LIKE "%{gt}%";
                                """
            elif tp == 4:
                com = f"""
                                SELECT mail FROM users
                                WHERE phone_number = "{gt}";
                                """
            elif tp == 5:
                com = f"""
                                SELECT mail FROM users
                                WHERE gender = "{gt}";
                                """
            elif tp == 6:
                com = f"""
                                SELECT mail FROM users;
                                """

            con = sqlite3.connect("dbUsers.sqlite")
            cur = con.cursor()
            cur.execute(com)
            lst = list(map(lambda x: x[0], cur.fetchall()))
            con.close()
            try:
                send_emails(lst, self.tm.text(), self.body.toPlainText(), mail, password)
                QMessageBox.information(self, " ", "Рассылка успешно отправлена!")
            except:
                QMessageBox.critical(self, " ", "Рассылка прервалась из-за ошибки")
            self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('deleteForm.ui', self)  # Загружаем дизайн
        self.delBtn.clicked.connect(self.delete)
        self.findB.clicked.connect(self.findd)

    def findd(self):
        self.table2.clear()
        self.table2.setRowCount(0)
        self.table2.setColumnCount(0)
        tp = self.chB.currentIndex()
        gt = self.inp.text()
        com = ""
        if tp == 0:
            if gt.isdigit():
                com = f"""
                        SELECT * FROM users
                        WHERE id = {int(gt)};
                        """
            else:
                QMessageBox.critical(self, " ", "Введите число")
        elif tp == 1:
            com = f"""
                    SELECT * FROM users
                    WHERE name = "{gt}";
                    """
        elif tp == 2:
            com = f"""
                    SELECT * FROM users
                    WHERE surname = "{gt}";
                    """
        elif tp == 3:
            com = f"""
                    SELECT * FROM users
                    WHERE mail LIKE "%{gt}%";
                    """
        elif tp == 4:
            com = f"""
                    SELECT * FROM users
                    WHERE phone_number = "{gt}";
                    """
        elif tp == 5:
            com = f"""
                    SELECT * FROM users
                    WHERE gender = "{gt}";
                    """

        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute(com)
        lst = cur.fetchall()
        con.close()
        if len(lst):
            self.table2.setRowCount(len(lst))
            self.table2.setColumnCount(len(lst[0]) - 1)
            self.table2.setHorizontalHeaderLabels(
                ("name", "surname", "patronymic", "mail", "phone_number", "date_of_birth", "gender"))
            for i, j in enumerate(lst):
                for i2, k in enumerate(j[1:]):
                    self.table2.setItem(i, i2, QTableWidgetItem(k))
            self.table2.resizeColumnsToContents()

    def delete(self):
        f = 0
        tp = self.chB.currentIndex()
        gt = self.inp.text()
        com = ""
        if tp == 0:
            if not gt.isdigit():
                QMessageBox.critical(self, " ", "Введите число")
                f = 1
            else:
                com = f"""
                DELETE FROM users
                WHERE id = {int(gt)};
                """
        elif tp == 1:
            com = f"""
            DELETE FROM users
            WHERE name = "{gt}";
            """
        elif tp == 2:
            com = f"""
            DELETE FROM users
            WHERE surname = "{gt}";
            """
        elif tp == 3:
            com = f"""
            DELETE FROM users
            WHERE mail LIKE "%{gt}%";
            """
        elif tp == 4:
            com = f"""
            DELETE FROM users
            WHERE phone_number = "{gt}";
            """
        elif tp == 5:
            com = f"""
            DELETE FROM users
            WHERE gender = "{gt}";
            """

        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute(com)
        con.commit()
        con.close()
        self.close()
        if not f:
            QMessageBox.information(self, " ", "Контакт удален")
        self.inp.clear()


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addForm.ui', self)  # Загружаем дизайн
        self.addBtn.clicked.connect(self.crt)
        self.wm.setAutoExclusive(False)
        self.m.setAutoExclusive(False)

    def crt(self):
        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        try:
            f, n, s = self.fns.text().split()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО через пробел")
        else:
            mail = self.mail.text()
            tfnm = self.tfnm.text()
            dbb = self.dateb.text()
            gender = "Ж" if self.wm.isChecked() else "М" if self.m.isChecked() else "-"
            if not "@" in mail:
                QMessageBox.warning(self, "Ошибка", "Введите правильный mail")
            elif tfnm == "+7":
                QMessageBox.warning(self, "Ошибка", "Введите правильный номер телефона")
            else:
                cur.execute(f'''INSERT INTO users(name, surname, patronymic, mail, phone_number, date_of_birth, gender) 
                VALUES ("{n}", "{f}", "{s}", "{mail}", "{tfnm}", "{dbb}", "{gender}")''')
                con.commit()
        self.close()
        self.fns.clear()
        self.mail.clear()
        self.tfnm.setText("+7")
        self.dateb.setDateTime(QDateTime(2000, 1, 1, 10, 20))
        self.wm.setChecked(False)
        self.m.setChecked(False)
        con.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.addB.clicked.connect(self.add)
        self.updateB.clicked.connect(self.updatee)
        self.cleanB.clicked.connect(self.cleann)
        self.deleteB.clicked.connect(self.delete)
        self.createB.clicked.connect(self.createe)

        self.d1 = AddDialog()
        self.d2 = DeleteDialog()
        self.d3 = MailingDialog()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('dbUsers.sqlite')
        self.db.open()
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('users')
        self.model.select()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        # self.table.hideColumn(0)
        self.table.verticalHeader().setVisible(0)

    def add(self):
        self.d1.show()

    def cleann(self):
        con = sqlite3.connect("dbUsers.sqlite")
        cur = con.cursor()
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM sqlite_sequence")
        con.commit()
        con.close()

    def createe(self):
        self.d3.createDialog()

    def delete(self):
        self.d2.show()

    def updatee(self):
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('users')
        self.model.select()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
