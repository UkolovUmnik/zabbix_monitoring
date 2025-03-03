from os import system
from sys import argv
try:
    import requests
except:
    system("pip install requests")
try:
    from bs4 import BeautifulSoup
except:
    system("pip install bs4")
    from bs4 import BeautifulSoup
    

ip_transmitter=argv[1]
#ip_transmitter='192.168.1.251'
try:
    html=requests.get('http://'+ip_transmitter+'/status.xml')
    html.encoding="windows-1251"
except Exception as ex:
    print('0')
    exit
else:    
   # print('Забрал страницу')

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        PowerOutput=float(soup.find("param_value0").get_text())
        print('PowerOutput='+str(PowerOutput))
    except Exception as ex:
        print('0')
        
    try:               
        PowerReflect=float(soup.find("param_value1").get_text())
        print('PowerReflect='+str(PowerReflect))
    except Exception as ex:
        print('0')
        
    try:                 
        Modulation=float(soup.find("param_value12").get_text())
        print('Modulation='+str(Modulation))
    except Exception as ex:
        print('0')

    try:     
        Temperature=float(soup.find("param_value3").get_text())
        print('Temperature='+str(Temperature))
    except Exception as ex:
        print('0')

