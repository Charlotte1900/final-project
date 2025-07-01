
import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import sys

from mainform import *

class MainForm(QWidget):
    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()
        self.setWindowTitle(name)
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.setFixedSize(570,550)   # 设置窗体大小
        self.setStyleSheet("background-color:white")

        pix = QPixmap('login.PNG')

        admin_logo=QPixmap('admin.png')
        admin_logo=admin_logo.scaled(70,70)

        password_logo = QPixmap('pswd.png')
        password_logo = password_logo.scaled(70, 70)

        lb1 = QLabel(self)
        lb1.setGeometry(200, 10, 500, 110)
        lb1.setPixmap(pix)

        lb2 = QLabel(self)
        lb2.setGeometry(70, 150, 70, 70)
        lb2.setPixmap(admin_logo)

        lb4 = QLabel(self)
        lb4.setGeometry(70, 250, 70, 70)
        lb4.setPixmap(password_logo)

        line= QLabel(self)
        line.setGeometry(70, 225, 420, 1)
        line.setStyleSheet("background-color:gray")

        line2 = QLabel(self)
        line2.setGeometry(70, 325, 420, 1)
        line2.setStyleSheet("background-color:gray")
        # self.account = QLabel(self)
        # self.account.setGeometry(QtCore.QRect(180, 150, 100, 70))
        # font = QtGui.QFont()
        # font.setFamily("AcadEref")
        # font.setPointSize(20)
        # self.account.setFont(font)
        # self.account.setObjectName("account")
        # self.account.setText("账号")

        self.account_input=QLineEdit(self)
        self.account_input.setGeometry(QtCore.QRect(170, 150, 300, 60))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(20)
        self.account_input.setFont(font)
        self.account_input.setStyleSheet("border-width:0;border-style:outset")
        self.account_input.setObjectName("account_input")



        # self.passwd = QLabel(self)
        # self.passwd.setGeometry(QtCore.QRect(180, 240, 100, 70))
        # font = QtGui.QFont()
        # font.setFamily("AcadEref")
        # font.setPointSize(20)
        # self.passwd.setFont(font)
        # self.passwd.setObjectName("account")
        # self.passwd.setText("密码")

        self.passwd_input = QLineEdit(self)
        self.passwd_input.setGeometry(QtCore.QRect(170, 250, 300, 60))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(20)
        self.passwd_input.setFont(font)
        self.passwd_input.setObjectName("passwd_input")
        self.passwd_input.setStyleSheet("border-width:0;border-style:outset")
        self.passwd_input.setEchoMode(QLineEdit.Password)

        self.login = QPushButton(self)
        self.login.setGeometry(QtCore.QRect(130, 380, 300, 60))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        self.login.setFont(font)
        self.login.setObjectName("login_btn")
        self.login.setStyleSheet("background-color:#419BF9;color:white")
        self.login.setText("登录")

        self.login.clicked.connect(self.word_get)

        self.login = QPushButton(self)
        self.login.setGeometry(QtCore.QRect(240, 480, 100, 60))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        self.login.setFont(font)
        self.login.setStyleSheet("background-color:gray;color:white")
        self.login.setText("注册")

        #self.login.clicked.connect(self.word_get)

    def word_get(self):
        login_user = self.account_input.text()
        login_password = self.passwd_input.text()
        if login_user == 'admin' and login_password == '123456':

            mainForm.close()
        elif login_user == 'user' and login_password == '123456':
            user_ui.show()
            mainForm.close()

        else:
            QMessageBox.warning(self,
                                "警告",
                                "用户名或密码错误！",
                                QMessageBox.Yes)
            self.passwd_input.setText("")
            self.passwd_input.setFocus()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = MainForm('智能证件照生成系统')

    user_ui=user_mainWindow()
    mainForm.show()
    sys.exit(app.exec_())


