import sys
import keyboard
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
from ContactBook import Ui_MainWindow_ContactBook


class Ui_ContactBook(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.uicontactbook = Ui_MainWindow_ContactBook()
        self.uicontactbook.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.conn = sqlite3.connect("ContactBookDB.db")
        self.c = self.conn.cursor()
        self.CREAT_DATABASE()
        self.uicontactbook.insert.clicked.connect(self.INSERT)
        self.uicontactbook.update.clicked.connect(self.UPDATE)
        self.SHOWTABLE()
        self.uicontactbook.refresh.clicked.connect(self.Refresh)
        self.uicontactbook.deletee.clicked.connect(self.DELETE)
        self.uicontactbook.clear.clicked.connect(self.CLEAR)
        self.uicontactbook.help_btn.clicked.connect(self.help)
        self.show()

    def mousePressEvent(self, evt):
        self.oldpos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldpos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldpos = evt.globalPos()

    def keyPressEvent(self, a0):
        if keyboard.is_pressed("enter") == True:
            self.SEARCH()

    def CREAT_DATABASE(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS ContactInfo(
        ID INT PRIMARY KEY NOT NULL,
        Name TEXT,
        Email TEXT,
        PhoneNumber TEXT,
        Address TEXT
        );
        """)

    def Refresh(self):
        self.c.execute(
            """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo""")
        cc = self.c.fetchall()
        self.uicontactbook.tableWidget.setRowCount(len(cc))
        for i in range(len(cc)):
            for j in range(5):
                self.uicontactbook.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(cc[i][j])))

    def SHOWTABLE(self):

        self.c.execute(
            """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo""")
        cc = self.c.fetchall()
        self.uicontactbook.tableWidget.setRowCount(len(cc)+1)
        for i in range(len(cc)):
            for j in range(5):
                self.uicontactbook.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(cc[i][j])))

    def INSERT(self):
        ID = self.uicontactbook.ID.text()
        Name = self.uicontactbook.name.text()
        Email = self.uicontactbook.email.text()
        PhoneNumber = self.uicontactbook.phone.text()
        Address = self.uicontactbook.address.toPlainText()

        if ID and Name and Email and PhoneNumber and Address != "":
            try:
                self.c.execute("""INSERT INTO ContactInfo VALUES ('%d', '%s', '%s', '%s', '%s')""" % (
                    int(ID), Name, Email, PhoneNumber, Address))
                self.conn.commit()
                msg = QMessageBox.information(
                    self, "INSERT Finished", "User information successfully added")
                self.uicontactbook.ID.setText("")
                self.uicontactbook.name.setText("")
                self.uicontactbook.email.setText("")
                self.uicontactbook.phone.setText("")
                self.uicontactbook.address.setPlainText("")

                self.c.execute(
                    """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo""")
                cc = self.c.fetchall()
                for i in range(len(cc)):
                    for j in range(5):
                        self.uicontactbook.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(cc[i][j])))

                self.uicontactbook.tableWidget.setRowCount(len(cc) + 1)

            except:
                msg = QMessageBox.information(
                    self, "INSERT Error", "User information cannot added !!!")
        else:
            msg = QMessageBox.warning(
                self, "Error", "Please fill in all the required fields !")

    def UPDATE(self):
        ID = self.uicontactbook.ID.text()
        Name = self.uicontactbook.name.text()
        Email = self.uicontactbook.email.text()
        PhoneNumber = self.uicontactbook.phone.text()
        Address = self.uicontactbook.address.toPlainText()

        checkedname = self.uicontactbook.searchbyname.isChecked()
        checkedid = self.uicontactbook.searchbyid.isChecked()

        if ID or Name != "":
            try:
                if ((checkedid == True) and (checkedname == False)):
                    self.c.execute("""UPDATE ContactInfo SET Name='%s', Email='%s', PhoneNumber='%s', Address='%s' WHERE ID='%d' """
                                   % (Name, Email, PhoneNumber, Address, int(ID)))
                    self.conn.commit()

                    self.c.execute(
                        """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo WHERE ID = '%s'""" % (ID))
                    cc = self.c.fetchall()
                    msg = QMessageBox.information(
                        self, "UPDATE Finished", "User information successfully edited")
                    self.uicontactbook.tableWidget.setRowCount(len(cc))
                    for i in range(len(cc)):
                        for j in range(5):
                            self.uicontactbook.tableWidget.setItem(
                                i, j, QTableWidgetItem(str(cc[i][j])))

                elif ((checkedname == True) and (checkedid == False)):
                    msg = QMessageBox.information(
                        self, "UPDATE Error", "User cannot update by ID !!!")

            except:
                msg = QMessageBox.information(
                    self, "UPDATE Error", "User cannot edited !!!")

        else:
            msg = QMessageBox.warning(
                self, "Error", "Please fill in all the required fields !")

    def DELETE(self):

        ID = self.uicontactbook.ID.text()
        Name = self.uicontactbook.name.text()
        checkedname = self.uicontactbook.searchbyname.isChecked()
        checkedid = self.uicontactbook.searchbyid.isChecked()
        if ID or Name != "":
            try:
                if ((checkedid == True) and (checkedname == False)):
                    self.c.execute(
                        """DELETE FROM ContactInfo WHERE ID = '%s'""" % (ID))
                    self.conn.commit()
                    msg = QMessageBox.information(
                        self, "DELETE Finished", "User information successfully deleted")
                    self.SHOWTABLE()

                elif ((checkedname == True) and (checkedid == False)):
                    msg = QMessageBox.information(
                        self, "DELETE Error", "User cannot deleted by ID !!!")

            except:
                msg = QMessageBox.information(
                    self, "DELETE Error", "User cannot deleted !!!")

        else:
            msg = QMessageBox.warning(
                self, "Error", "Please fill in all the required fields (ID / Name) !")

    def CLEAR(self):
        self.uicontactbook.ID.setText("")
        self.uicontactbook.name.setText("")
        self.uicontactbook.email.setText("")
        self.uicontactbook.phone.setText("")
        self.uicontactbook.address.setPlainText("")
        self.SHOWTABLE()

    def SEARCH(self):
        checkedname = self.uicontactbook.searchbyname.isChecked()
        checkedid = self.uicontactbook.searchbyid.isChecked()
        searchby = self.uicontactbook.search.text()
        searchbyid = searchby
        searchbyname = searchby

        if ((checkedname == True) and (checkedid == False)):

            self.c.execute(
                """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo WHERE Name = '%s'""" % (searchbyname))
            cc = self.c.fetchall()

            for i in cc:
                i0 = i[0]
                i1 = i[1]
                i2 = i[2]
                i3 = i[3]
                i4 = i[4]

                self.uicontactbook.ID.setText(str(i0))
                self.uicontactbook.name.setText(str(i1))
                self.uicontactbook.email.setText(str(i2))
                self.uicontactbook.phone.setText(str(i3))
                self.uicontactbook.address.setPlainText(str(i4))
                break

            if (searchby != ""):
                self.c.execute((
                    """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo WHERE Name = '%s'""" % (
                        searchbyname)))
                cc = self.c.fetchall()
                self.uicontactbook.tableWidget.setRowCount(len(cc))
                for i in range(len(cc)):
                    for j in range(5):
                        self.uicontactbook.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(cc[i][j])))
                self.uicontactbook.search.setText("")

            elif (searchbyname == ""):
                self.SHOWTABLE()

        elif ((checkedid == True) and (checkedname == False)):

            self.c.execute(
                """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo WHERE ID = '%s'""" % (searchbyid))
            cc = self.c.fetchall()

            for i in cc:
                i0 = i[0]
                i1 = i[1]
                i2 = i[2]
                i3 = i[3]
                i4 = i[4]

                self.uicontactbook.ID.setText(str(i0))
                self.uicontactbook.name.setText(str(i1))
                self.uicontactbook.email.setText(str(i2))
                self.uicontactbook.phone.setText(str(i3))
                self.uicontactbook.address.setPlainText(str(i4))
                break
            if (searchby != ""):
                self.c.execute((
                    """SELECT ID, Name, Email, PhoneNumber, Address FROM ContactInfo WHERE ID = '%s'""" % (searchbyid)))
                cc = self.c.fetchall()
                self.uicontactbook.tableWidget.setRowCount(len(cc))
                for i in range(len(cc)):
                    for j in range(5):
                        self.uicontactbook.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(cc[i][j])))
                self.uicontactbook.search.setText("")

            elif (str(searchbyid) == ""):
                self.SHOWTABLE()

    def help(self):

        message_box = QtWidgets.QMessageBox()

        message_box.setWindowTitle("Developer information")
        message_box.setWindowIcon(QtGui.QIcon('royal_lionn.ico'))
        message_box.setIcon(QMessageBox.Information)

        message_box.setText("Developer : Amin Jafari\n"
                            "---------------------------------\n"
                            "Gmail : Aminjjjeffrey@gmail.com\n")
        message_box.exec_()

    def pushbutton(self):
        self.uidicerollingsimulator.dice1.clicked.connect(
            self.rolling_dice_player1)
        self.uidicerollingsimulator.dice2.clicked.connect(
            self.rolling_dice_player2)
        self.uidicerollingsimulator.settime.clicked.connect(self.set_time)
        self.uidicerollingsimulator.resetgame1.clicked.connect(
            self.rest_player1)
        self.uidicerollingsimulator.resetgame2.clicked.connect(
            self.rest_player2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = Ui_ContactBook()
    sys.exit(app.exec_())
