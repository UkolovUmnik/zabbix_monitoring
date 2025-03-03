from os import system
from sys import argv
try:
    import requests
except:
    system("pip install requests")
    import requests
try:
    from bs4 import BeautifulSoup
except:
    system("pip install bs4")
    from bs4 import BeautifulSoup
try:
    import lxml
except:
    system("pip install lxml")
    import lxml

ip_transmitter=argv[1]

try:
    xml=requests.get('http://'+ip_transmitter+'/status.xml')
    xml.encoding="windows-1251"
except Exception as ex:
    print('0')
    exit
else:    
   # print('Забрал страницу')
    try:
        soup = BeautifulSoup(xml.content, 'xml')
    except Exception as ex:
        pass
    
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

