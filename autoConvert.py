import logging

import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from datetime import date
import wx
import os       
import pyodbc 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import mysql.connector as msql
from mysql.connector import Error
from PySide6.QtWidgets import(
    QApplication,
    QMainWindow,
    QCheckBox,
    QComboBox,
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
    mainLabName = ''
    emailEnabled = 1
    usingFile = ''
    
    #-------------------
    emailAddress=''
    DBServer =''
    DBName =''
    DBuser=''
    DBpassword=''
    sender = "nikitaskorobogatovvw@gmail.com"


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
##############################################################
        self.labNametxt = QLabel("Select LabName:")
        self.LabList = QComboBox(self)
        self.LabList.addItem("FSNSTech")
        self.LabList.addItem("IEHInc")
        self.LabList.addItem("Silliker")
        self.sendemail = QCheckBox("Enable send Email",self)
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.labNametxt)
        self.layout2.addWidget(self.LabList)
        self.layout2.addSpacing(50)
        self.layout2.addWidget(self.sendemail)
        
        ###################################################
        
        self.button = QPushButton("Start Convert")
        self.button.clicked.connect(self.display_selection)
##############################################################
        
   
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
        self.vlay.addLayout(self.layout2)
        # self.vlay.addSpacing(20)
        # self.vlay.addWidget(self.sendemail)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout1)
        self.vlay.addSpacing(20)
        self.vlay.addWidget(self.button)
        central_widget = QWidget()
        central_widget.setLayout(self.vlay)
        self.setCentralWidget(central_widget)

#################################################################
    def display_selection(self):
        self.openData()
        selection = self.LabList.currentText()
        self.emailEnabled = self.sendemail.checkState()
        self.mainLabName = selection
        for path in self.uploadFileNames:
            self.mainCSVPath = path
            head, tail = os.path.split(self.mainCSVPath)
            self.mainCSVName = tail
            self.mainName = tail.replace('.csv','')
            self.changeDBName(self.mainName)
            self.insertData()
            self.desctexts()
    def openData(self):
        file = open('./config.csv')
        csvreader = csv.reader(file)
        header=[]
        header = next(csvreader) 
        colNum = len(header)
        rows=[]
        for row in csvreader:
            rows.append(row)
        autoSetting =rows[0]
        self.emailAddress = autoSetting[0]
        self.DBServer = autoSetting[1]
        self.DBName = autoSetting[2]
        self.DBuser = autoSetting[3]
        self.DBpassword = autoSetting[4]
        
    def selectFiles(self):
       
        filetypes = (
                ('CSV files', '*.csv'),
                # ('All files', '*.*')
                
            )

        self.uploadFileNames = fd.askopenfilenames(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
        # self.mainCSVPath = self.uploadFileNames[1]
        
            # self.uploadBtn.setText(self.mainCSVPath)
           

    def desctexts(self):
        self.txt = self.mainCSVPath
        self.desctext.setText(self.txt)
    def sendEmail(self):
        print('Sending Email.....')
        # Email configuration
        smtp_server = 'sandbox.smtp.mailtrap.io'
        smtp_port = 587
        sender_email = 'convertCSV@gmail.com'
        # sender_password = 'your_email_password'
        recipient_email = self.emailAddress
        subject = 'Test Email'
        message = 'This is a test email sent from Python.'
        html = '''
            <html>
                <body style="text-align:center; background-color:black; color:white;">
                    <h1 >File Convert Result</h1>
                    <h2>Hello, welcome to your report!</h2>
                    <h3>At '''+ str(self.CreatedTime) +''' ,Some products were added or updated from '''+ str(self.mainCSVName)+''' file.</h3>
                    <p>'''+ str(self.allRowCount) +''' products were changed in your database!</p>
                    <p>'''+str(self.insertedCount) +''' products were inserted in your database!</p>
                    <p>'''+str(self.updatedCount) +''' products were updated in your database!</p>
                    <p>'''+str(self.failedCount) +''' products were failed in your database!</p>
                    
                </body>
            </html>
            '''

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        # msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(html, "html"))
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start a secure connection
            server.login("b12b658d4ac33f", "b53b654fcf6289")  # Login to the server
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
            print('Email sent successfully!')
      
        
        
    def changeDBName(self,dbName):
        if(dbName.find("BonelessBeef")!=-1):
            self.mainName = "BonelessBeef_MicroTest"
        if(dbName.find("Fat")!=-1):
            self.mainName = "FinishedProd_FatTest"
        if(dbName.find("FinishedProd")!=-1):
            self.mainName = "FinishedProd_MicroTest"
        if(dbName.find("BonelessBison")!=-1):
            self.mainName = "BonelessBison_MicroTest"
        if(dbName.find("BisonFat")!=-1):
            self.mainName = "Bison_FatTest"
        if(dbName.find("GroundBison")!=-1):
            self.mainName = "GroundBison_MicroTest"
    def insertData(self):
        ################  create database   ############################
        try:
            # conn = msql.connect(host='localhost',database='sdrk', user='root',  
            #                     password='') 
           
            # conn = pyodbc.connect('Driver={SQL Server};'
            #             'Server=pc-kcy;'
            #             'Database=SDRKS;'
            #             # 'UID=SDRSDB;'
            #             # 'PWD=!@QWas12;'
            #             'Trusted_Connection=yes;'
            #                 )
            str = '\'Driver={SQL Server};\''+' \'Server='+self.DBServer+';\''+' \'Database='+self.DBName + ';\''+' \'UID='+self.DBuser +';\'' + ' \'PWD='+self.DBpassword +';\''
            conn = pyodbc.connect(str)
            cursor = conn.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)
            
        logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s")  
        ##################    file open   ##############################
        
       
        
        # stmt = "SHOW TABLES LIKE "+self.mainName
        # cursor.execute(stmt)
        # result = cursor.fetchone()
        file = open(self.mainCSVPath)
        csvreader = csv.reader(file)
        header=[]
        j=0
        Sample = 0
        header = next(csvreader) 
        colNum = len(header)
        num = len(header)
        extra = ",FileID INT NULL, LastUpdated VARCHAR(50) NULL, UpdatedBy  VARCHAR(50) NULL, Remarks VARCHAR(50) NULL)" 
        # if result == false:
    # if there is no table in database, create dateabase
        i = 0
        CreateDBQuery ="CREATE TABLE IF NOT EXISTS "+ self.mainName + " ("
        for columns in header:
            i=i+1
            if columns =='':
                columns = "UnNamed_" + str(i)
            if columns =='Material_Description':
                columns = "Material_Code"
            if ( columns =='E_coli_O157_H7' or  columns =='E_Coli_O157_H7') :
                columns = "E_coli_0157_H7"
            if columns =='E_Coli_O157_H7_Cl':
                columns = "E_Coli_0157_H7_Cl"
            if columns =='Status':
               columns = "StatusN"
            strs = columns + '  varchar(100)'
            if i == num:
                CreateDBQuery = CreateDBQuery + ' ' + strs + extra
            else:
                CreateDBQuery = CreateDBQuery + ' ' +  strs + ','
        CreateDBQuery = CreateDBQuery.replace('-','_')
        cursor = conn.cursor()
        # sqlrs = 'DROP TABLE IF EXISTS '+ self.mainName +';'
        # cursor.execute(sqlrs)
        print('Creating table....')

        cursor.execute(CreateDBQuery)
        print("Table is created....")

# then now there is an database in Database#
# insert data into table
        
        for heads in header:
            j=j+1
            if heads =='Sample_Number':
                Sample = j-1
            
        rows=[]
        dataExtra = ",FileID , LastUpdated , UpdatedBy  , Remarks ) " 
        updateDataExtra = ",FileID =%s , LastUpdated =%s , UpdatedBy=%s  , Remarks=%s " 
        for row in csvreader:
            rows.append(row)
        insertNumber =1
        updateNumber =1
        isbool = 0
        for row in rows:
            # rows.append(row)
            
            numSample = row[Sample]
            numSample = numSample.replace('-','_')
            isNewQuery = "Select * from "+ self.mainName +" where Sample_Number = '"+numSample + "'" 
            isNew = cursor.execute(isNewQuery)
            data="error" #initially just assign the value
            for i in cursor:
                data=i #if cursor has no data then loop will not run and value of data will be 'error'
            if data=="error":
                query ='insert into '+ self.mainName + ' ('
                j=0
                for heads in header:
                    j = j+1
                    if heads =='':
                        heads = "UnNamed_" + str(j)
                    if heads =='Material_Description':
                       heads = "Material_Code"
                    if ( heads =='E_coli_O157_H7' or  heads =='E_Coli_O157_H7') :
                        heads = "E_coli_0157_H7"
                    if heads =='E_Coli_O157_H7_Cl':
                        heads = "E_Coli_0157_H7_Cl"
                    if heads =='Status':
                        heads = "StatusN"
                    if j == num:
                        query= query + heads + dataExtra
                    else:
                        query= query + heads +','
                query= query +' VALUES ' 
                today = date.today()
                insertTime = today.strftime("%d/%m/%Y") 
                # for row in rows:
                # self.allRowCount = self.allRowCount + 1
                row = row[0:colNum]
                row[Sample] = row[Sample].replace('-','_')
                s=str(row)
                s = s.replace('[','(')
                s = s.replace(']',' ')
                squery = query + s + ',\''+'ID'+'\',' +'\''+ insertTime +'\',' +'\''+ self.mainCSVName +'\''+ ',\'NULL\' )' 
                squery = squery.replace('-','_')
                try:
                    cursor.execute(squery)
                    # self.updatedCount =self.updatedCount + 1
                    self.insertedCount =self.insertedCount + 1
                except Error as e:
                    self.failedCount = self.failedCount + 1
                    print ("Warning::",e)
                    pass
                sss = str(insertNumber) +" data inserted in Database!"
                insertNumber = insertNumber+1
                print (sss)
                self.desctext.setText(self.txt)
                conn.commit()
                print("**********************************************")
            else:
                today = date.today()
                insertTime = today.strftime("%d/%m/%Y") 
                row = row[0:colNum]
                if(isbool == 0):
                    header.append("FileID")
                    header.append("LastUpdated")
                    header.append("UpdatedBy")
                    header.append("Remarks")
                    isbool = 1
                row.append("ID")
                row.append(insertTime)
                row.append(self.mainCSVName)
                row.append("NULL")
                query = "update "+ self.mainName + " Set "
                j=0
                
                for heads in header:
                    if heads =='':
                        heads = "UnNamed_" + str(j)
                    if heads =='Material_Description':
                       heads = "Material_Code"
                    if ( heads =='E_coli_O157_H7' or  heads =='E_Coli_O157_H7') :
                        heads = "E_coli_0157_H7"
                    if heads =='E_Coli_O157_H7_Cl':
                        heads = "E_Coli_0157_H7_Cl"
                    if heads =='Status':
                        heads = "StatusN"
                    updatequery = query+ heads + "=%s  where Sample_Number = %s"
                    updatequery = updatequery.replace('-','_')
                    val = row[j]
                    j = j+1
                    
                    try:
                        cursor.execute(updatequery,(val,numSample))
                        
                    except Error as e:
                        self.failedCount = self.failedCount + 1
                        print ("Warning::",e)
                        pass
           
                self.updatedCount =self.updatedCount + 1
                sss = str(updateNumber) +" data updated in Database!"
                updateNumber = updateNumber+1
                print (sss)
                self.desctext.setText(self.txt)
                conn.commit()
                print("**********************************************")
                        
            
            
            
        self.desctext.setText('Converting completed! ') 
        today = date.today()
        self.CreatedTime = today.strftime("%d/%m/%Y")
        self.allRowCount = self.insertedCount + self.updatedCount + self.failedCount
        mainquery ="insert into File_Uploaded(Filename,UploadTimeStamp,LabName,TotalRecords,RecordsProcessed,\
            RecordsDuplicate,Remarks,RecordsInserted,RecordsUpdated,Recordsfailed) Values "
        values=[ self.mainCSVName,self.CreatedTime,self.mainLabName,self.allRowCount,self.allRowCount-self.failedCount,'0',"NuLL",self.insertedCount,
            self.updatedCount,self.failedCount]
        strVal= str(values)
        strVal = strVal.replace('[','(')
        strVal = strVal.replace(']',') ')
        mainquery = mainquery + strVal
        cursor.execute(mainquery)
        print("Log file exactly updated")
        conn.commit()
        str1 = self.mainCSVName +' file was inserted in database'
        str2 = str(self.insertedCount) +' products were inserted in database'
        str3 = str(self.updatedCount) +' products were updated in database'
        str4 = str(self.failedCount) +' file were failed in database'
        str5 = "email was sent to " + self.emailAddress
        
        if (self.emailEnabled.value== 2):
            self.sendEmail() 
            logging.info(str5) 
      
        logging.info(str1)
        logging.info(str2)
        logging.info(str3)
        logging.info(str4)
 
        
        #     rows.append(row)
        # #################  create table ################################
        # num = len(header)
        # i = 0
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


