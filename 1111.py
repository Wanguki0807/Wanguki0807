from bs4 import BeautifulSoup
import re
# import urllib2

url = "./source/index.html"
page = open(url,encoding='utf-8')
soup = BeautifulSoup(page.read(),'html.parser')
texts = str(soup)
