from sys import argv
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

#ip_transmitter='192.168.1.251'
ip_transmitter=argv[1]

session=requests.session()
#login='admin'
#password='root'
url='http://'+ip_transmitter+'/web/getcurrent'
#page=session.get(url=url, auth=(login, password))
page=session.get(url)
page.encoding="windows-1252"
soup = BeautifulSoup(page.text, 'html.parser')
#print(page.text)
        
channel_rad = soup.find("e2servicename").text
channel_rad.strip()
print('ChanelRadio='+str(channel_rad))
