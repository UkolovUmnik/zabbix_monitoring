from sys import argv
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

#ip_transmitter='192.168.1.251'
ip_transmitter=argv[1]

html = requests.get('http://'+ip_transmitter, auth=HTTPBasicAuth('admin', '1234567'))
html.encoding="windows-1251" 
#print('Забрал страницу')
            
soup = BeautifulSoup(html.text, "html.parser")
spisok=soup.find_all('span', class_="style14")
                    
PowerOutput=spisok[0].get_text()
print('PowerOutput='+str(PowerOutput))
                
PowerReflect=spisok[2].get_text()
print('PowerReflect='+str(PowerReflect))
                
Modulation=spisok[7].get_text()
print('Modulation='+str(Modulation))
                
Temperature = soup.find("td", class_="style11").get_text()
print('Temperature='+str(Temperature))

