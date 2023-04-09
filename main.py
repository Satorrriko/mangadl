# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designertNAxjb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import Crypto.Cipher.AES as AES
import binascii
import re
import requests
import json
import threading
import os

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerTqknrb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 492)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(220, 10, 71, 21))
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 40, 281, 192))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 10, 201, 20))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(90, 240, 71, 21))
        self.tableView_2 = QTableView(self.centralwidget)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setGeometry(QRect(10, 270, 281, 192))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 240, 69, 22))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 240, 121, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.ui_get_chapter)
        self.pushButton_2.clicked.connect(self.ui_download_chapter)
        self.comboBox.currentIndexChanged.connect(self.ui_set_dltable)
        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Get info", None))
        self.lineEdit.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u8bdd", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5377", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u756a\u5916", None))

        self.label.setText("")
    # retranslateUi



    def ui_get_chapter(self):
        type_list = {
            1: '话',
            2: '卷',
            3: '番外',
        }
        self.name = self.lineEdit.text()
        self.chapter_list = get_chapter_list(self.name)
        # set tableview
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Type', 'Title', 'ID'])
        for chapter in self.chapter_list['groups']['default']['chapters']:
            # print(chapter)
            item = QStandardItem(type_list[chapter['type']])
            item2 = QStandardItem(chapter['name'])
            item3 = QStandardItem(chapter['id'])
            model.appendRow([item, item2, item3])
            # item3 add to tableview
        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()

    def ui_set_dltable(self):
        # print('ui_set_dltable')
        dl_type = self.comboBox.currentIndex()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Type', 'Page', 'Progress', 'Links'])
        
        for chapter in self.chapter_list['groups']['default']['chapters']:
        
            if str(chapter['type']) == str(dl_type + 1):
                QApplication.processEvents()
                self.label.setText('Getting chapter ' + chapter['name'] + '...')
                thread = threading.Thread(target=self.get_page_list, args=(self.name, chapter, model))
                # self.fname, self.page_list = get_page_list(self.name, chapter['id'])
                thread.start()
                
                
        thread.join()
        
        self.tableView_2.setModel(model)
        self.tableView_2.resizeColumnsToContents()
        self.tableView_2.resizeRowsToContents()
    def get_page_list(self, name, chapter, model):
        url = 'https://api.copymanga.site/api/v3/comic/' + name + '/chapter/' + chapter['id']
        res = requests.get(url).json()
        item = QStandardItem(chapter['name'])
        item2 = QStandardItem(str(len(res['results']['chapter']['contents'] )))
        item4 = QStandardItem(json.dumps(res['results']['chapter']['contents']))
        model.appendRow([item, item2, QStandardItem('0'), item4])
        self.fname = res['results']['comic']['name']
        # return res['results']['comic']['name'], res['results']['chapter']['contents']            
    def ui_download_chapter(self):
        # print("download_chapter")
        # get tableview2 content
        # get tableview2 content
        model = self.tableView_2.model()
        for row in range(model.rowCount()):
            item1 = model.item(row, 0).text()
            item2 = model.item(row, 1).text()
            url = json.loads(model.item(row, 3).text())
            if os.path.isdir('./' + self.fname + '/' + item1):
                pass
            else:
                os.makedirs('./' + self.fname + '/' + item1)
            # threading.Thread(target=self.download_chapter, args=(self.fname, item1, url)).start()
            self.download_chapter(self.fname, item1, url)
            # download_chapter(name = self.fname, chapter = item1, page_list = url)
    def download_chapter(self, name, chapter, page_list):
        page = 1
        for img in page_list:
            thread = threading.Thread(target=self.download, args=(img['url'], name, chapter, page))
            thread.start()
            QApplication.processEvents()

            page += 1
        thread.join()

    def download(self, url, name, chapter, page):
        # print(url)
        r = requests.get(url, stream=True)
        if os.path.isdir('./' + name+ '/' + chapter):
            pass
        else:
            os.makedirs('./' + name+ '/' + chapter)
        with open(name + '/' + chapter + '/' + str(page) + '.jpg', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                QApplication.processEvents()
                if chunk:
                    f.write(chunk)
                    f.flush()
        self.label.setText(str(page) + ' of ' + chapter)
        table = self.tableView_2
        model = table.model()
        for row in range(model.rowCount()):
            if model.item(row, 0).text() == chapter:
                c = int(model.item(row, 2).text())
                c += 1
                model.item(row, 2).setText(str(c))
def aes_decode(data):
    key = 'xxxmanga.woo.key'.encode('utf_8')
    iv = data[:16].encode('utf_8')
    cipher = binascii.a2b_hex(data[16:])
    mode = AES.MODE_CBC
    aes = AES.new(key, mode, iv)
    cplistb = aes.decrypt(cipher)
    cplist = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',"",cplistb.decode('utf-8'))
    return cplist

def get_chapter_list(name):
    r = requests.get('https://www.copymanga.site/comic/' + name + '/chapters')
    chapter_list = r.json()['results']
    return json.loads(aes_decode(chapter_list))

def get_page_list(name, id):
    url = 'https://api.copymanga.site/api/v3/comic/' + name + '/chapter/' + id
    res = requests.get(url).json()
    return res['results']['comic']['name'], res['results']['chapter']['contents']
    
def download_chapter(name, chapter, page_list):
    page = 1
    for img in page_list:
        thread = threading.Thread(target=download, args=(img['url'], name, chapter, page))
        thread.start()
        thread.join()
        page += 1
    
def download(imgurl, name, chapter, page):
    r = requests.get(imgurl)
    if os.path.isdir('./' + name+ '/' + chapter):
        pass
    else:
        os.makedirs('./' + name+ '/' + chapter)
    with open(name + '/' + chapter + '/' + str(page).zfill(4) + '.jpg', 'wb') as f:
        f.write(r.content)
        f.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())