from sys import argv
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

ip_transmitter=argv[1]

session=requests.session()
url='http://'+ip_transmitter+'/Status.asp'
page=session.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
variants = soup.find_all("tr", class_='cell_out', nowrap="")
        
for i in range(0,7):
    variants.pop()
for i in range(-4,-1):
    variants.pop(i)
variant=variants.pop()
        
j=0
for i in variant:
    j=j+1
    if j==2:
        channel_rad=i.text

channel_rad.strip()
print('ChanelRadio='+str(channel_rad))
