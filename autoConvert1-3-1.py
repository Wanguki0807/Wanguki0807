
import csv
import mysql.connector as msql
from mysql.connector import Error
import sys
from datetime import date
import wx
import os
import pyodbc 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
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
    uploadFileNames = []
    mainCSVPath = ''
    mainName = ''
    colNum = 0
    txt = ''
    mainCSVName = ''
    CreatedTime=''
    allRowCount=0
    insertedCount =0
    updatedCount = 0
    failedCount = 0
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
        # def get_path(wildcard):
        #     app = wx.App(None)
        #     style = wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
        #     dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
        #     if dialog.ShowModal() == wx.ID_OK:
        #         path = dialog.GetPath()
        #     else:
        #         path = None
        #     dialog.Destroy()
        #     return path
        # self.mainCSVPath =get_path("CSV files (*.csv)|*.csv")
        # head, tail = os.path.split(self.mainCSVPath)
        filetypes = (
                ('CSV files', '*.csv'),
                # ('All files', '*.*')
                
            )

        self.uploadFileNames = fd.askopenfilenames(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
        # self.mainCSVPath = self.uploadFileNames[1]
        for path in self.uploadFileNames:
            self.mainCSVPath = path
            head, tail = os.path.split(self.mainCSVPath)
            self.mainCSVName = tail
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
                      'Server=AMSBBSQL2016;'
                      'Database=SDRS;'
                      'UID=SDRSDB;'
                      'PWD=!@QWas12;'
                    # 'Trusted_Connection=yes;'
                      )
            cursor = conn.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)
        ##################    file open   ##############################
        file = open(self.mainCSVPath)
        csvreader = csv.reader(file)
        header=[]
        header = next(csvreader) 
        colNum = len(header)
        rows=[]
        for row in csvreader:
            rows.append(row)
        #################  create table ################################
        num = len(header)
        i = 0
        CreateDBQuery ="CREATE TABLE "+ self.mainName + " ("
        for columns in header:
            i=i+1
            if columns =='':
                columns = "UnNamed_" + str(i)
            strs = columns + '  varchar(100)'
            if i == num:
                CreateDBQuery = CreateDBQuery + ' ' + strs + ')'
            else:
                CreateDBQuery = CreateDBQuery + ' ' +  strs + ','
        CreateDBQuery = CreateDBQuery.replace('-','_')
        cursor = conn.cursor()
        sqlrs = 'DROP TABLE IF EXISTS '+ self.mainName +';'
        cursor.execute(sqlrs)
        print('Creating table....')

        cursor.execute(CreateDBQuery)
        print("Table is created....")

        query ='insert into '+ self.mainName + ' ('
        j=0
        for heads in header:
            j = j+1
            if heads =='':
                heads = "UnNamed_" + str(j)
            if j == num:
                query= query + heads +')'
            else:
                query= query + heads +','
        query= query +' VALUES ' 
        number = 1   
        for row in rows:
            self.allRowCount = self.allRowCount + 1
            row = row[0:colNum]
            s=str(row)
            s = s.replace('[','(')
            s = s.replace(']',')')
            squery = query + s
            squery = squery.replace('-','_')
            try:
                cursor.execute(squery)
                self.updatedCount =self.updatedCount + 1
                self.insertedCount =self.insertedCount + 1
            except Error as e:
                self.failedCount = self.failedCount + 1
                print ("Warning::",e)
                pass
            sss = str(number) +" data inserted in Databae!"
            number = number+1
            print (sss)
            self.desctext.setText(self.txt)
            conn.commit()

        
        self.desctext.setText('Converting completed! ') 
        today = date.today()
        self.CreatedTime = today.strftime("%d/%m/%Y")
        cursor.execute("insert into File_Uploaded(Filename,UploadTimeStamp,LabName,TotalRecords,RecordsInserted,RecordsUpdated,Recordsfailed,Remarks) values (?,?,?,?,?,?,?,?)",\
            self.mainCSVName,self.CreatedTime,'labName',self.allRowCount,self.insertedCount,self.updatedCount,self.failedCount,'')
        print("Log file exactly updated")
        conn.commit()

        conn.close()
        print('Converting completed')
        self.mainCSVPath = ''
        self.CreatedTime=''
        self.allRowCount =0
        self.insertedCount = 0
        self.updatedCount = 0
        self.failedCount = 0
        self.mainName = ''
        self.colNum = 0
        self.txt = ''
app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(100,100,600,300)
window.show()
app.exec()


