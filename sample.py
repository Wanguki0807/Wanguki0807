import requests
import re
import wget
from pathlib import Path
import sys
import os
import wx
import shutil
from zipfile import ZipFile
from bs4 import BeautifulSoup
import zipfile
from PySide6.QtWidgets import(
    QApplication,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTextEdit,
    QMessageBox,
    QCheckBox,
    QSpinBox,
    QComboBox,
)

class MainWindow(QMainWindow):
    currencyArray=["$","€","£"]
    currency="$"
    destr = ""
    chkst = False
    redirectText ="Add to cart"
    pricePercent = 50
    beforePrice = 0
    mainUrl ="https://www.w3schools.com/"
    proName =""
    source = "./source"
    mainImgPath =""
    descTxt=""
    mainText =""
    mainLen= 0
    path = "./shop"
    subStringArray=[]
    mainhrefArray=[]
    localhrefArray=[]
    sourceArray=[]
    Price=0
    smallUrl = "venkateshbaddela.github.io/"
    mainLen =len(mainUrl)
    assets_dir =path+"/assets/"
    rootpath = "./shop"
    zipname = "./shop.zip"
    completeArray = []
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Download Urls")
        self.copy()
        #***************************
        self.text = QLabel(" Redirect Urls")
        self.lineEdit = QLineEdit(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.lineEdit)
        self.lineEdit.editingFinished.connect(self.insertUrl)

         #***************************
        self.proNameTxt = QLabel("Product Name:")
        self.proNameLine = QLineEdit(self)
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.proNameTxt)
        self.layout1.addWidget(self.proNameLine)
        self.proNameLine.editingFinished.connect(self.proNameEdit)

        #*********************************

        self.redirectTxt = QLabel("Button Text:")
        self.redirectLine = QLineEdit(self)
        self.layout6 = QHBoxLayout()
        self.layout6.addWidget(self.redirectTxt)
        self.layout6.addWidget(self.redirectLine)
        self.redirectLine.editingFinished.connect(self.redirectEdit)

         #***************************
        self.pricetxt = QLabel("Price:")
        self.priceLine = QSpinBox(minimum=0,maximum = 10000000, value=0, prefix='')
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.pricetxt)
        self.layout2.addWidget(self.priceLine)
        self.priceLine.valueChanged.connect(self.priceChanged)
         #***************************
        self.checktxt1 = QLabel("Discount:",self)
        self.checkbox = QCheckBox(self)
        
        self.checktxt = QLabel("Currency",self)
        self.combobox = QComboBox(self)
        self.prectxt = QLabel("Percent",self)
        self.percentSpin = QSpinBox(minimum=0,maximum = 100, value=0, prefix='')
        self.hlaym = QHBoxLayout()
        self.hlaym.addWidget(self.checktxt1)
        self.hlaym.addWidget(self.checkbox)
        self.hlaym.addSpacing(40)
        self.hlaym.addWidget(self.checktxt)
        self.hlaym.addWidget(self.combobox)
        self.hlaym.addSpacing(40)
        self.hlaym.addWidget(self.prectxt)
        self.hlaym.addWidget(self.percentSpin)
        self.combobox.addItems(self.currencyArray)
        self.combobox.currentIndexChanged.connect(self.selectionchange)
        self.percentSpin.valueChanged.connect(self.percent)
        self.checkbox.stateChanged.connect(self.checkstate)
         #***************************
        self.desctxt = QLabel("Description")
        self.desctext = QTextEdit(self)
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.desctxt)
        self.layout3.addWidget(self.desctext)
        self.desctext.textChanged.connect(self.desctexts)

         #***************************
        self.filetxt = QLabel("Upload File:")
        self.uploadBtn = QPushButton("Choose",self)
        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(self.filetxt)
        self.layout4.addWidget(self.uploadBtn)
        self.uploadBtn.clicked.connect(self.upload)

         #***************************
        self.filetxt1 = QLabel("")
        self.downBtn = QPushButton("Download to Zip",self)
        self.layout5 = QHBoxLayout()
        self.layout5.addWidget(self.filetxt1)
        self.layout5.addWidget(self.downBtn)
        self.downBtn.clicked.connect(self.download)


        #**********************************
        self.vlay = QVBoxLayout(self)
        self.vlay.addLayout(self.layout)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout1)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout2)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.hlaym)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout3)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout6)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout4)
        self.vlay.addSpacing(20)
        self.vlay.addLayout(self.layout5)
        
        central_widget = QWidget()
        central_widget.setLayout(self.vlay)
        self.setCentralWidget(central_widget)
        
        #*******************************

    def checkstate(self):
        if self.checkbox.isChecked() == True:
            self.chkst = True
        else:
            self.chkst = False
                       


    def desctexts(self):
        self.destr = self.desctext.toPlainText()


    def selectionchange(self,i):
        self.currency = self.currencyArray[i]

    def insertUrl(self):
        self.mainUrl = self.lineEdit.text()

    def priceChanged(self,value):
        self.Price = str(value)

    def percent(self,value):
        self.pricePercent = value
        self.beforePrice = float((int(self.Price))*100/(100-int(self.pricePercent)))

    def redirectEdit(self):
        self.redirectText = self.redirectLine.text()

    def proNameEdit(self):
        self.proName = self.proNameLine.text()
        
    
    def download(self):
        
        
        self.validateUrl()
        self.makeindex()
        self.changeProName()
        self.changeDestr()
        self.changeRedirectWord()
        self.setRedirectUrl()
        self.changePrice()
        
    def copy(self):
        if os.path.exists("./shop"):
             shutil.rmtree("./shop")
        shutil.copytree(self.source, os.getcwd()+"./shop")
    def changeRedirectWord(self):
        
        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_=re.compile("price-cart__btn-img"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
               strs = str(element.next)
               strs =strs.replace("  ","")
               strs =strs.replace("\n","")
               name = self.redirectText
               self.mainText = self.mainText.replace(strs,name)

    def setRedirectUrl(self):
        
        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_=re.compile("price-cart__btn btn--orange"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
                strs = str(element)
                strss = 'class="price-cart__btn btn--orange"'
                self.mainText = self.mainText.replace(strss,'class="price-cart__btn btn--orange" onclick=window.location.href="{}"'.format(self.mainUrl))
                #self.mainText = self.mainText.replace(changeStr,strs1)


    def upload(self):

        
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
       
        self.mainImgPath =get_path("All files(*.*)|*.*|JPG files (*.jpg)|*.jpg|BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png")
        self.uploadBtn.setText(self.mainImgPath)
        url = "./source/index.html"
        page = open(url,encoding='utf-8')
        sous = BeautifulSoup(page.read(),'html.parser')
        self.mainText = str(sous)

        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_="img-main")
        if len(find_by_class) == 0:
             print("No Elements are found under this class name")
        else:
            for element in find_by_class:
                strs = str(element)
                href = re.findall(r'src=[\'"]?([^\'" >]+)',strs)
                shutil.copy(self.mainImgPath,"./shop/"+href[0])
                



    def validateUrl(self):    
       
        url = "./source/index.html"
        page = open(url,encoding='utf-8')
        sous = BeautifulSoup(page.read(),'html.parser')
        self.mainText = str(sous)


    def makeindex(self):
        path = self.path
        try: 
             os.mkdir(path) 
        except OSError as error: 
             print(error) 
        if os.path.exists(path+"\index.html"):
            os.remove(path+"\index.html")
        else:
             print("New file will creat")
        

    def changeProName(self):
        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_=re.compile("price-main__heading"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
               strs = str(element.string)
               name = self.proName
               self.mainText = self.mainText.replace(strs,name)
         



    def changePrice(self):

        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_=re.compile("price-box__main-new"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
               strs =  str(element.string)
               name = self.currency+str(self.Price)
               self.mainText = self.mainText.replace(strs,name)

       
        find_by_class = soup.find_all(class_=re.compile("price-box__main-discount"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
               strs =  str(element.string)
               name = str(self.pricePercent)+"%"
               self.mainText = self.mainText.replace(strs,name)

        find_by_class1 = soup.find_all(class_=re.compile("price-box__old"))
        if len(find_by_class1) == 0:
            print("No Elements are found under this class name")
        else:
            for element1 in find_by_class1:
               if self.chkst == True:
                    strs1 = str(element1.string)
                    name1 =self.currency + str(self.beforePrice)
                    self.mainText= self.mainText.replace('style ="display:none;"',"")
                    self.mainText = self.mainText.replace(strs1,name1)
                
               else:
                    strs1 = str(element1)
                    strs2 = strs1.replace("class=","style ='display:none;' class=")
                    self.mainText = self.mainText.replace(strs1,strs2)
          
        self.writeHtmlText()          
      



    def changeDestr(self):
        soup = BeautifulSoup(self.mainText, 'html.parser')
        find_by_class = soup.find_all(class_=re.compile("price-txt"))
        if len(find_by_class) == 0:
            print("No Elements are found under this class name")
        else:
            for element in find_by_class:
               strs = str(element.string)
               name =str(self.destr)
               self.mainText = self.mainText.replace(strs,name)

    def writeHtmlText(self):
        f = open(self.path+"\index.html", "a",encoding="utf-8")
        try: 
         f.write(self.mainText)
        except OSError as error: 
         print(error) 
        f.close
        self.zip_compression_tree(self.rootpath,self.zipname)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("DownLoad is finished")
        msgBox.setWindowTitle("Complete!")
        msgBox.exec()

    def zip_compression_tree(self,root, zip_name):
        with zipfile.ZipFile(zip_name, 'w') as z:
            for root, dirs, files in os.walk(root):
                for file in files:
                    z.write(os.path.join(root, file))
                for directory in dirs:
                    z.write(os.path.join(root, directory))

        if os.path.exists('./shop.zip'):
           # os.unlink("./shop")
            print("ZIP file created")
        else:
            print("ZIP file not created")
    
            

   
        
app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(100,100,600,600)
window.show()
app.exec()
