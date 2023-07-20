
# Python program to find a HTML tag
# that contains certain text Using BeautifulSoup
 
# Importing library
import requests
from bs4 import BeautifulSoup
import re
classArray=[]
str1 = " class="
str2=" style='display:none;' class="
mainContent = requests.get("https://hergom-medical.com/collections/aspiracion-y-succion/products/aspirador-quirurgico-de-flemas-y-secreciones-de-20-l-x-minuto-modelo-7a-23b-marca-hergom-aspiradores-1?utm_source=FB_ADS&utm_medium=ASPIRADOR_7A-23B&utm_campaign=HERGOM_GENERAL2023&utm_id=HER_1344_FB_ADS") 
soup = BeautifulSoup(mainContent.text, 'html.parser')
cp=".jpg"
#jss = [i.start() for i in re.finditer(cp, mainContent.text)]
num = mainContent.text.count(cp)
app = []
if num == 0:
    print("No Elements are found under this class name")
else:
    i = 0
    while i < num:
        if i == 0:
             app.append(mainContent.text.index(cp))
        else :
             app.append(mainContent.text.index(cp,app[i-1]+10))
        i += 1
print (app)
    #for element in jss:
    #    array =str(element)
   #     changed=array.replace(str1,str2)
    #    print (array)


    *************************************

  def changeWebp(self):
        soup = BeautifulSoup(self.maintext, 'html.parser')
        cp=".webp"
        #jss = [i.start() for i in re.finditer(cp, mainContent.text)]
        num = self.maintext.count(cp)
        app = []
        if num == 0:
            print("No Elements are found under this class name")
        else:
            u = 0
            while u < num:
                if u == 0:
                    app.append(self.maintext.index(cp))
                else :
                    app.append(self.maintext.index(cp,app[u-1]+10))
                u += 1
            let = "./"
            k=0
            for i in app:
                k = i   
                while   k >i-200:
                    k-=1
                    lets = self.mainContent.text[k:k+2]
                    if let == lets : 
                        subStr= self.mainContent.text[k:i]
                        self.maintext = self.maintext.replace("./assets","https://hergom-medical.com")
                        pass