import requests
import os
import re
from threading import Thread
from queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QStringListModel
import sys
import time

from PyQt5.QtWidgets import QMessageBox

from qt.layout import Ui_MainWindow as UIM
from 下载组件 import *

song_download = kugou_download()

def download_mp3(name):
    song_name_json = song_download.download_name(name)
    i = 1
    song_list = []
    for song in song_name_json['data']['lists']:
        file_name = str(i) + '.' + song['FileName'].replace(
            '<em>', '').replace('</em>', '').replace('<\\/em>', '')
        song_list.append(file_name)
        i += 1
    return song_list, song_name_json



class UIM_Version(UIM, QtWidgets.QWidget):
    send_args = pyqtSignal(str, int)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)  # 因为继承关系，要对父类初始化
        self.download_list = []

    def setupFunction(self):
        self.pushButton.clicked.connect(self.send)
        self.pushButton_2.clicked.connect(self.onButtonClick)
        self.pushButton_3.clicked.connect(self.open_tip)
        self.pushButton_4.clicked.connect(self.open_dir)
        self.listView_2.clicked.connect(self.remove)
        self.listView.clicked.connect(self.clickedlist)
        self.pushButton_5.clicked.connect(self.download_go)

    def onButtonClick(self):
        # 此处发送信号的对象是button1按钮
        qApp = QtWidgets.QApplication.instance()
        qApp.quit()

    def download_go(self):
        if not self.download_list:
            QtWidgets.QMessageBox.critical(self,'提示','下载列表为空！',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            for dow in self.download_list:
                nmb = int(dow.split('.')[0]) - 1
                meg = song_download.download_main(self.jsons['data']['lists'][nmb]['FileHash'], True)
                self.handleDisplay(meg)
                time.sleep(5)
            self.handleDisplay('下载完成')

    def handleDisplay(self,data):
        self.textBrowser.append(data)   #在指定的区域显示提示信息
        self.cursor=self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)  #光标移到最后，这样就会自动显示出来
        QtWidgets.QApplication.processEvents()  #一定加上这个功能，不然有卡顿


    def remove(self, qModelIndex):
        r = self.download_list[int(qModelIndex.row())]
        print(r)
        if r in self.download_list:
            self.download_list.remove(r)
            self.handleDisplay('下载列表删除：{}'.format(r))
        slm = QStringListModel()
        slm.setStringList(self.download_list)
        self.listView_2.setModel(slm)

    def clickedlist(self, qModelIndex):
        if not self.li[int(qModelIndex.row())] in self.download_list:
            self.download_list.append(self.li[int(qModelIndex.row())])
            self.handleDisplay('下载列表添加：{}'.format(self.li[int(qModelIndex.row())]))
            slm = QStringListModel()
            slm.setStringList(self.download_list)
            self.listView_2.setModel(slm)

    def send(self):
        http_url = self.lineEdit.text()  # 获取第一个文本框中的内容
        if http_url == '':
            self.msg("提示", "请输入关键词")
        else:
            self.li, self.jsons = download_mp3(http_url)
            slm = QStringListModel()
            slm.setStringList(self.li)
            self.listView.setModel(slm)


    def open_tip(self):
        QtWidgets.QMessageBox.about(None, "使用帮助", '<p style="color:green;">本软件是由赣州市电子工业技术学校 20秋计算机应用一班 袁长峰开发的/开源的软件，仅用于交流学习，请勿用于商业用途</p> \
        <p>1.输入歌名，点击搜索</p> \
        <p>2.选择需要下载的歌曲</p> \
        <p>3.单击开始下载，即可下载歌词与音乐</p><br> \
        <a href="https://github.com/chenyuqin-dlut/nhentai-imgcollect" rel="nofollow">GitHub项目地址</a>')

    def msg(self, title, msg):
        QtWidgets.QMessageBox.information(self, title, msg, QtWidgets.QMessageBox.Yes)


    def open_dir(self):
        path = os.getcwd() + r'\音乐'
        if not os.path.exists(path):
            os.mkdir('音乐')
        os.system("explorer.exe %s" % path)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIM_Version()
    ui.setupUi(MainWindow)
    ui.setupFunction()
    ui.handleDisplay("如果你不知道该如何使用本软件，请点击“使用说明”按钮查看帮助")
    MainWindow.show()
    sys.exit(app.exec_())