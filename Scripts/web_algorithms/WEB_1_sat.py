from sys import argv
import requests
from bs4 import BeautifulSoup

ip_transmitter=argv[1]
channel_rad=''
session=requests.session()
login='admin'
password='root'
url='http://'+ip_transmitter+'/cgi-bin/decoder.cgi'
try:
    page=session.get(url=url, auth=(login, password))
    page.encoding="windows-1252"
    soup = BeautifulSoup(page.text, 'html.parser')
    variants = soup.find_all("input", {"name":"service_name"})
    #print(variants)
    for i in variants:
        channel_rad=i.attrs['value']
    if channel_rad=="":
        channel_rad=str(parametr('.1.3.6.1.4.1.38295.31.4.1.0','public',ip_transmitter, 161))
        begin=int(channel_rad.find("=")+2)
        end=begin+15
        channel_rad=channel_rad[begin:end]
        channel_rad.strip()
    channel_rad=channel_rad.strip()
    print('ChanelRadio='+str(channel_rad))
except Exception as ex:
    print('ChanelRadio='+'ошибка')


