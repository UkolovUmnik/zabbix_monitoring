from sys import argv
import requests
from bs4 import BeautifulSoup


#ip_transmitter='192.168.1.252'
ip_transmitter=argv[1]
session=requests.session()
#login='admin'
#password='root'
url='http://'+ip_transmitter+'/tcf?cgi=show&$path=/Service'
#page=session.get(url=url, auth=(login, password))
page=session.get(url)
page.encoding="windows-1252"
soup = BeautifulSoup(page.text, 'html.parser')
#print(page.text)
#variants = soup.find_all("input", {"name":"service_name"})
variant = soup.find_all("script")
        
perem=0
for i in range(0,2):
    rezult=variant.pop().text
    #print(rezult+'\n')
    if i==1:
        perem=rezult.find("Current Audio PID','")
        #print(perem)
        rezult=int(rezult[perem+21:perem+24])
        #print(channel_rad)
        break
if rezult==294:
    channel_rad='294 - RetroFM4'
else:
    channel_rad="Unknown"
channel_rad.strip()
print('ChanelRadio='+str(channel_rad))
