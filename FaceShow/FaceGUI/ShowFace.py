# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from FaceGUI.GetImageData import Main
from PyQt5 import QtCore, QtGui, QtWidgets

# 控制台输出
class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

# 主对话框
class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)
        sys.stdout = Stream(newText = self.onUpdateText)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("多人脸识别程序")
        MainWindow.resize(1110, 981)
        self.initial_path = None
        self.image_path = None
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btOpenFile = QtWidgets.QPushButton(self.centralwidget)
        self.btOpenFile.setGeometry(QtCore.QRect(20, 50, 101, 41))
        self.btOpenFile.setObjectName("btOpenFile")
        self.btRecognition = QtWidgets.QPushButton(self.centralwidget)
        self.btRecognition.setGeometry(QtCore.QRect(20, 110, 101, 41))
        self.btRecognition.setObjectName("btRecognition")
        self.btShowCatalog = QtWidgets.QPushButton(self.centralwidget)
        self.btShowCatalog.setGeometry(QtCore.QRect(150, 110, 101, 41))
        self.btShowCatalog.setObjectName("btShowCatalog")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 210, 241, 501))
        self.listView.setObjectName("listView")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(290, 20, 791, 701))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 789, 699))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(30, 20, 731, 661))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{background:white;}")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btShowImage = QtWidgets.QPushButton(self.centralwidget)
        self.btShowImage.setGeometry(QtCore.QRect(150, 50, 101, 41))
        self.btShowImage.setObjectName("btShowImage")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.ensureCursorVisible()
        self.textEdit.setLineWrapColumnOrWidth(5000)
        # self.textEdit.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.textEdit.setGeometry(QtCore.QRect(20, 730, 1061, 191))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.btOpenFile.clicked.connect(lambda :self.openImage())
        self.btShowImage.clicked.connect(lambda :self.openFile())
        self.btRecognition.clicked.connect(self.Recognition)
        self.listView.clicked.connect(self.Clicked)
        self.btShowCatalog.clicked.connect(self.showCatalog)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "多人脸识别程序"))
        self.btOpenFile.setText(_translate("MainWindow", "打开图片"))
        self.btRecognition.setText(_translate("MainWindow", "开始识别"))
        self.btShowCatalog.setText(_translate("MainWindow", "显示图片目录"))
        self.btShowImage.setText(_translate("MainWindow", "打开图片目录"))

    # 打开图片
    def openImage(self):
        file_path = QFileDialog.getOpenFileName(None, "选择图片", 'UnknownImage',"*.jpg;;*.png;;All Files(*)")
        if file_path == None:
            QMessageBox.information(None,'提示','文件为空，请重新操作')
        else:
            self.image_path = file_path[0]

        self.showImage()

    # 打开文件夹
    def openFile(self):
        file_path = QFileDialog.getExistingDirectory(None, "选取文件夹", '../')
        if file_path == None:
            QMessageBox.information(None,'提示','文件为空，请选择打开图片目录')
        else:
            self.initial_path = file_path

    # 识别图片
    def Recognition(self):

        if self.image_path:
            print('开始识别...')
            QMessageBox.information(None, "正在识别..", "开始识别！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            Main(self.image_path)
            self.image_path = 'KnownImage/' + os.listdir('KnownImage')[0]
            self.showImage()
            # QMessageBox.information(None, "正在识别..", "识别完毕！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            print('识别完毕...')

        else:
            QMessageBox.warning(None,"错误","图片为空，请先打开要识别的图片")

    # 单击显示图片
    def Clicked(self,qModelIndex):
        self.image_path = self.initial_path + '/' + self.qList[qModelIndex.row()]
        self.showImage()

    # 显示图片文件夹list
    def showCatalog(self):
        self.itemModel = QStringListModel(self.centralwidget)
        self.qList = []
        if self.initial_path:
            for item in os.listdir(self.initial_path):
                self.qList.append(item)
        else:
            QMessageBox.warning(None,'错误','文件为空，请选择打开图片目录')
        self.itemModel.setStringList(self.qList)
        self.listView.setModel(self.itemModel)

    # 显示图片
    def showImage(self):
        jpg = QPixmap(self.image_path).scaled(self.label.width(),self.label.height())
        if jpg.isNull():
            QMessageBox.warning(None, '错误', '请正确选择图片')
        else:
            self.label.setPixmap(jpg)

    # 显示输出
    def onUpdateText(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())