from sys import argv
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

#ip_transmitter='192.168.1.251'
ip_transmitter=argv[1]

session=requests.session()
login='admin'
password='root'
url='http://'+ip_transmitter+'/status.asp'
page=session.get(url=url, auth=(login, password))
page.encoding="windows-1252"
#print(page.text)
soup = BeautifulSoup(page.text, 'html.parser')
variants=soup.find_all("td", class_="StatusDis", width="151", align="left", valign="middle", bgcolor="#EAEAEA")
#print(variants)
#for i in variants:
#print(i.getText())
#print(len(variants))
for i in range(1,len(variants)+1):
    rezult=variants.pop()
    #print(str(i))
#print(rezult)
channel_rad=rezult.getText()
channel_rad.strip()
print('ChanelRadio='+str(channel_rad))
