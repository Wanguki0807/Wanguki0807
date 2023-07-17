import requests
import os
import re
import wget
from pathlib import Path
import sys
import os
from zipfile import ZipFile
import zipfile

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
firsturl = "https://www.comme-avant.bio/pages/coffret-solaire-nutri-co-x-comme-avant"
mainUrl = "www.comme-avant.bio"
rootpath = "./clone"
zipname = "./clone.zip"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Download Urls")

       # self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QPushButton("download")
    #    self.text = QLabel("Insert Urls")
        self.lineEdit = QLineEdit(self)
        self.progressbar = QProgressBar(self)
        self.layout = QVBoxLayout(self)
    #    self.layout.addWidget(self.text)
        self.button.setCheckable(True)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)
       # self.text.setStyleSheet('padding-left: 100px; padding-top: 90px;')
        #self.button.clicked.connect(self.magic)
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.lineEdit.editingFinished.connect(self.urlChanged)
    def urlChanged(self):
        firsturl = self.lineEdit.text
        indices_object = re.finditer(pattern='/', string=firsturl)
        indices = [index.start() for index in indices_object]
        betNum = indices[2]
        betNum1 = indices[1]
        mainUrl = firsturl[betNum1:betNum]
    def the_button_was_clicked(self):
        completeArray=[]
        allAmount = len(realhrefArray)
        percent = 0
        for href in realhrefArray:
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
            try: 
                
        #    savefile = open(subFile,"bw")
                if "https:"  in subString or "http:" in subString :
                    sub = subString
                else:
                    sub = subString.replace("//","https://")
                    source = href.replace(assets_dir,sub)
            #target = savefile.name
            #assert os.path.isfile(target)
        #  print (href)
            
            except OSError as error: 
                print(error) 
            source = source.replace("_{width}x","")
            
            if source in completeArray:
                pass
            else:
                try:
                    response = wget.download(source,subFile)
                    completeArray.append(source)
                except OSError as error:
                    pass 
            print ("oneDown")
            percent = percent +1
            self.progressbar.setValue = percent / (allAmount+1)
        print ("download finished")
        zip_compression_tree(rootpath,zipname)
        changeText()

#the required first parameter of the 'get' method is the 'url':
mainLen = len(mainUrl)
mainContent = requests.get(firsturl)  
#parsed = urlparse.urlparse(x)
#print the response text (the content of the requested file):
#print(x.text)

directory = "clone"
  
# Parent Directory path
parent_dir = "./"
 
# Path
path = os.path.join(parent_dir, directory)
assets_dir = path+"/assets" 
try: 
    os.mkdir(path) 
except OSError as error: 
    print(error) 
if os.path.exists(path+"\index.html"):
  os.remove(path+"\index.html")
else:
  print("The file does not exist")


realhref=""
realhrefArray = []
subString = ""
hrefArray = re.findall(r'src=[\'"]?([^\'" >]+)', mainContent.text)
for  ref in hrefArray:
    if mainUrl in ref:
       
        num = ref.rindex(mainUrl)+mainLen
        subString = ref [0:num]
        x = ref.replace(subString, assets_dir)
        realhref = x[num+1:len(x)]
      #  print(x)
        realhrefArray.append(x)

#print (realhrefArray)
def changeText():
    maintext = mainContent.text
    maintext = maintext.replace(subString,"./assets")
    #mainContent = maintext.parse()
    f = open(path+"\index.html", "a",encoding="utf-8")
    try: 
     f.write(maintext)
    except OSError as error: 
     print(error) 

    f.close
app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(400,300,500,200)
window.show()
app.exec()


def zip_compression_tree(root, zip_name):
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
