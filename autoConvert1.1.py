#please send me your skype address and Id. Please talk in there.. because , when I upload file to upwork, it 
#sends me  privacy message... I didn`t want stop my account. I sent you my Info before.

import csv
import mysql.connector as msql
from mysql.connector import Error
import sys
import wx
import os
import pyodbc 
from PySide6.QtWidgets import(
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QTextEdit,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
class MainWindow(QMainWindow):

    mainCSVPath = ''
    mainName = ''
    txt = ''
    def __init__(self):
        super().__init__()
##############################################################
        self.filetxt = QLabel("Upload File:")
        self.uploadBtn = QPushButton("Choose Folder",self)
        self.uploadBtn.setMinimumWidth(500)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.filetxt)
        self.layout.addWidget(self.uploadBtn)
        self.uploadBtn.clicked.connect(self.selectFiles)
################################################################
        self.desctxt = QLabel("Working Registry")
        self.desctext = QTextEdit(self)
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.desctxt)
        self.layout1.addWidget(self.desctext)
        # self.desctext.textChanged.connect(self.desctexts)

        self.vlay = QVBoxLayout(self)
        self.vlay.addLayout(self.layout)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout1)
        self.vlay.addSpacing(20)
        central_widget = QWidget()
        central_widget.setLayout(self.vlay)
        self.setCentralWidget(central_widget)

#################################################################
    def selectFiles(self):
        def get_path(wildcard):
            app = wx.App(None)
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
            else:
                path = None
            dialog.Destroy()
            return path
        self.mainCSVPath =get_path("CSV files (*.csv)|*.csv")
        head, tail = os.path.split(self.mainCSVPath)
        self.mainName = tail.replace('.csv','')
    
        self.desctexts()
        # self.uploadBtn.setText(self.mainCSVPath)
        self.insertData()

    def desctexts(self):
        self.txt = self.mainCSVPath
        self.desctext.setText(self.txt)
        








    def insertData(self):
        ################  create database   ############################
        try:
            # conn = msql.connect(host='localhost', user='root',  
            #                     password='')
           
            conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=RON\SQLEXPRESS;'
                      'Database=SDRS;'
                      'UID=SDRSDB;'
                      'PWD=!@QWas12;'
                      )
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE newDatabase")
                print("Database is created")
        except Error as e:
            print("Error while connecting to MySQL", e)
        ##################    file open   ##############################
        file = open(self.mainCSVPath)
        csvreader = csv.reader(file)
        header=[]
        header = next(csvreader)
        rows=[]
        for row in csvreader:
            rows.append(row)
        #################  create table ################################
        num = len(header)
        i = 0
        CreateDBQuery ="CREATE TABLE "+ self.mainName + " ("
        for columns in header:
            i=i+1
            strs = columns + '  varchar(100)'
            if i == num:
                CreateDBQuery = CreateDBQuery + ' ' + strs + ')'
            else:
                CreateDBQuery = CreateDBQuery + ' ' +  strs + ','
        try:
            conn = msql.connect(host='localhost', database='newDatabase', user='root', password='')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                sqlrs = 'DROP TABLE IF EXISTS '+ self.mainName +';'
                cursor.execute(sqlrs)
                print('Creating table....')

                cursor.execute(CreateDBQuery)
                print("Table is created....")

            query ='insert into '+ self.mainName + ' ('
            j=0
            for heads in header:
                j = j+1
                if j == num:
                    query= query + heads +')'
                else:
                    query= query + heads +','
            query= query +' VALUES ' 
            number = 1   
            for row in rows:
                
                s=str(row)
                s = s.replace('[','(')
                s = s.replace(']',')')
                squery = query + s
                cursor.execute(squery)
                
                sss = str(number) +" data inserted in Databae!"
                number = number+1
                print (sss)
                self.desctext.setText(self.txt)
                conn.commit()

            conn.close()
            self.desctext.setText('Converting completed! ') 
            print('Converting completed')
        except Error as e:
                    print("Error while connecting to MySQL", e)

app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(100,100,600,300)
window.show()
app.exec()


