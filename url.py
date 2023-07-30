import requests
import os
import re
import wget
from pathlib import Path
import sys
import os
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
)

class MainWindow(QMainWindow):
    payArray=["paypal","payment"]
    str1 = " class="
    str2=" style='display:none;' class="
    inUrl = ""
    rootpath = "./clone"
    zipname = "./clone.zip"
    mainContent = ""
    mainUrl = ""
    mainLen = 0
    path = "./clone"
    assets_dir = path+"/assets"
    hrefArray = []
    localhrefArray = []
    mainhrefArray = []
    subStringArray = []
    completeArray = []
    sourceArray = []
    price = ""
    redirectUrl = ""
    aTagArray =[]
    
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Download Urls")
        self.button = QPushButton("download")
       # self.button1 = QPushButton("PriceSet")
       # self.hlay1 = QHBoxLayout()
       # self.hlay1.addWidget(self.button)
       # self.hlay1.addWidget(self.button1)
        self.text = QLabel("Insert Urls")
        self.lineEdit = QLineEdit(self)
        self.redirect = QLabel("Redirect Urls")
        self.relineEdit = QLineEdit(self)
        self.textdown = QLabel("Ready to download")
        self.checkbox = QCheckBox("Remove Payments",self)
        #self.checkbox.setChecked(false)
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.progressBar.setValue(0)
        self.textEdit = QTextEdit(self) 
        self.layouts = QHBoxLayout(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.lineEdit)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.textdown)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.progressBar)
        self.layout.addSpacing(10)
        self.text1 = QLabel("Price:")
        self.priceEdit = QDoubleSpinBox(self)
        self.priceEdit.editingFinished.connect(self.priceChanged)
        self.hlay = QHBoxLayout()
        self.hlay.addWidget(self.text1)
        self.hlay.addWidget(self.priceEdit)
        self.layout.addLayout(self.hlay)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.redirect)
        self.layout.addWidget(self.relineEdit)
        self.relineEdit.editingFinished.connect(self.redirectChanged)
        self.layout.addWidget(self.checkbox)
        self.checkbox.stateChanged.connect(self.chkChanged)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.button)
        self.layouts.addLayout(self.layout)
        self.layouts.addWidget(self.textEdit)
        central_widget = QWidget()
        central_widget.setLayout(self.layouts)
        self.setCentralWidget(central_widget)
        self.button.clicked.connect(self.downloads)
        self.lineEdit.editingFinished.connect(self.urlChanged)

    def chkChanged(self):
        if self.checkbox.checkState == True:
            chkSt = True
        else:
            chkSt = False




    def setPaymentNone(self):

            soup = BeautifulSoup(self.maintext, 'html.parser')
            for pays in self.payArray:
                find_by_class = soup.find_all(class_=re.compile(pays))
            
                if len(find_by_class) == 0:
                    print("No Elements are found under this class name")
                else:
                    for element in find_by_class:
                        array =str(element)
                        changedarray=array.replace(self.str1,self.str2)
                        self.maintext = self.maintext.replace(array,changedarray)


    def priceChanged(self):
        self.price = str(self.priceEdit.text())


    def redirectChanged(self):
        self.redirectUrl = str(self.relineEdit.text())


    def setText(self, str):
        self.textEdit.setText(str)

        
    def setProgressBar(self, ints):
        self.progressBar.setValue(ints)


    def the_button_was_clicked(self):
        self.downloads()


    def urlChanged(self):
       self.inUrl = self.lineEdit.text()


    def setPrice(self):
        soup = BeautifulSoup(self.mainContent.text, 'html.parser')
        pattern = "itemprop=\"price\""
        text1 = self.maintext.find(pattern)
        cont = self.maintext[text1:text1+200]
        pos = cont.find("€") -5
        self.maintext = self.maintext.replace(self.maintext[text1+pos:text1+pos+6] ,self.price+"€")
       # self.textEdit.setText(self.inUrl)


    def downloads(self):
      #  self.textEdit.setText(self.inUrl)
        indices_object = re.finditer(pattern='/', string=self.inUrl)
        slashes = re.findall('/',self.inUrl)
        if len(slashes) >=2 :
            indices = [index.start() for index in indices_object]
            betNum = indices[2]
            betNum1 = indices[1]
            self.mainUrl = self.inUrl[betNum1+1:betNum]
        else :
             print("Url is not correct")
        self.mainContent = requests.get(self.inUrl) 
        self.mainLen = len(self.mainUrl)
        self.maintext = self.mainContent.text
        self.makeindex()


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
        self.findScrs()
        self.downloadfiles()


    def downloadfiles(self):
      
        soup = BeautifulSoup(self.mainContent.text, 'html.parser')
        allAmount = len(self.localhrefArray)
        percent = 0
        id = 0
        txt = ""
        for href in self.localhrefArray:
           
            head, tail = os.path.split(href)
            subFile = ""
            source = ""
            if "?" in href:
                numQuator = href.rindex("?")
                subFile = href[0:numQuator]
            else :
                subFile = href
            try: 
                Path(head).mkdir(parents=True, exist_ok=True) 
            except OSError as error: 
                print(error) 
            subFile = subFile.replace("_{width}x","")
            source = ""
            subArray = []
            so = self.sourceArray[id]
            if "https:"  in so or "http:" in so :
                sub = so
            else:
                sub = so.replace("//","https://") 
            
            source = sub.replace("_{width}x","")
            source = source.replace("es.comme-avant.bio","www.comme-avant.bio")
            if source in self.completeArray:
                pass
            else:
                try:
                    try:
                    # response = wget.download(source,subFile)
                        cp = self.mainhrefArray[id]
                        jss = [i.start() for i in re.finditer(cp, self.maintext)]
                        soup = BeautifulSoup(self.maintext, 'html.parser')
                        cp=self.mainhrefArray[id]
                        num = self.maintext.count(cp)
                        app = []
                        if num == 0:
                            print("No Elements are found under this")
                        else:
                            u = 0
                            while u < num:
                                if u == 0:
                                    app.append(self.maintext.index(cp))
                                else :
                                    app.append(self.maintext.index(cp,app[u-1]+1))
                                u+= 1                                                                    
                        let = ""
                        k=0
                        for i in app:
                            k = i   
                            while let != "<" and k >i-200:
                                k-=1
                                let = self.mainContent.text[k]
                            if self.mainContent.text[k+1] == "a":
                                self.maintext = self.maintext.replace(source,self.redirectUrl)
                                source = self.redirectUrl
                       # response = requests.get(source)
                       # open(subFile, "wb").write(response.content)
                       
                    except OSError as error:
                        pass
                    print (source)
                    self.completeArray.append(source)
                    percent = percent +1
                    txt =txt+ source+ "Successful downloaded \n"
                    
                except OSError as error:
                    pass 
                print ("One File is Downloaded Successfully")
                self.setText(txt)
                val = int(percent*100 / (allAmount+1))
                if id == len(self.localhrefArray):
                    val = 100
                    self.setProgressBar(val)
                
            id += 1
            
        print ("All files were downloaded")
        x =self.checkbox.checkState() 
        if  x.value == 2:
            self.setPaymentNone()
      #  self.setPrice()
        self.completeArray = []
       
        self.zip_compression_tree(self.rootpath, self.zipname)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("DownLoad is finished")
        msgBox.setWindowTitle("Complete!")
        msgBox.exec()
  
        f = open(self.path+"\index.html", "a",encoding="utf-8")
        try: 
         f.write(self.maintext)
        except OSError as error: 
         print(error) 
        f.close


    def findScrs(self):
        subString = ""
        hrefArray = re.findall(r'src=[\'"]?([^\'" >]+)',self.mainContent.text)
        hrefArray1 = re.findall(r'href=[\'"]?([^\'" >]+)',self.mainContent.text)
        hrefArray2 = re.findall(r'url[\'("]?([^\'") >]+)',self.mainContent.text)
        hrefArray3 = re.findall(r'url[\'("]?([^") >]+)',self.mainContent.text)
      #  soup = BeautifulSoup(self.maintext, 'html.parser')
      #  hrefArray4= [i.get('srcset') for i in soup.find_all('img', srcset=True)]

      #  hrefArray5 = re.findall(r'srcset=[\'"]?([^\'" >]+)',self.mainContent.text)
        """  subref = []
        for ref in hrefArray4:
            subref = ref.split(", ")
            hrefArray.append(subref)
        subref1 =[]
        for ref in hrefArray5:
            subref1 = ref.split(", ")
            hrefArray.append(subref)
         """
        for ref in hrefArray1:
            hrefArray.append(ref)
        for ref in hrefArray2:
            hrefArray.append(ref)
        for ref in hrefArray3:
            hrefArray.append(ref)
        for  ref in hrefArray:
            if self.mainUrl in ref:
              num = ref.rindex(self.mainUrl)+self.mainLen
              subString = ref [0:num]
              self.subStringArray.append(subString)
              x = ref.replace(subString, self.assets_dir)
              mainhref = ref[num:len(ref)]
              self.mainhrefArray.append(mainhref)
              self.localhrefArray.append(x)
              if ref[0] == "'":
                  ref = ref.replace(ref[0],"")
              self.sourceArray.append(ref)
              self.maintext = self.maintext.replace(subString,"./assets")
            else:
              subref = ""
              if len(ref)>7:
                subref = ref[0:8]
              if subref=="https://":
                  subString = "https:/"
                  mainhref = ref[7:len(ref)]
                  x = ref.replace(subString, self.assets_dir)
                  self.mainhrefArray.append(mainhref)
                  self.localhrefArray.append(x)
                  self.sourceArray.append(ref)
              #    self.maintext = self.maintext.replace(subString,"./assets")
              elif ref[0:1] == "//":
                    subString = "//"
                    mainhref = ref[2:len(ref)]
                    x = ref.replace(subString, self.assets_dir)
                    ref = ref.replace("//","https://")
                    self.mainhrefArray.append(mainhref)
                    self.localhrefArray.append(x)
                    self.sourceArray.append(ref)
                #    self.maintext = self.maintext.replace(subString,"./assets")
    
    def zip_compression_tree(self,root, zip_name):
        with zipfile.ZipFile(zip_name, 'w') as z:
            for root, dirs, files in os.walk(root):
                for file in files:
                    z.write(os.path.join(root, file))
                for directory in dirs:
                    z.write(os.path.join(root, directory))

            if os.path.exists('./clone.zip'):
                print("ZIP file created")
            #self.progressBar.value = 100
            else:
                print("ZIP file not created")

app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(400,300,500,200)
window.show()
app.exec()

