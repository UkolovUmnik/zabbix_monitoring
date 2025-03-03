from sys import argv
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

#ip_transmitter='192.168.1.251'
ip_transmitter=argv[1]

session=requests.session()
#login='ird'
#password='ird'
url='http://'+ip_transmitter+'/Status.asp'
#page=session.get(url=url, auth=(login, password))
page=session.get(url)
#page.encoding="windows-1252"
#print(page.text)
soup = BeautifulSoup(page.text, 'html.parser')
#variants = soup.find_all("tr", {"name":"service_name"})
variants = soup.find_all("tr", class_='cell_out', nowrap="")
#print(variants)
        
for i in range(0,7):
    variants.pop()
for i in range(-4,-1):
    variants.pop(i)
variant=variants.pop()
        
j=0
for i in variant:
    #print(i.text)
    j=j+1
    if j==2:
        channel_rad=i.text
#print('\n')
#print(rezult)

channel_rad.strip()
print('ChanelRadio='+str(channel_rad))
