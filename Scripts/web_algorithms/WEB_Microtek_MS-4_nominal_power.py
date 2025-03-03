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
        PercentPower=float(soup.find("power_level").get_text())
        print('PowerOutput='+str(PowerOutput))
    except Exception as ex:
        pass
    try:
        Pmax=float(soup.find("param_pmax").get_text())
        print('PowerOutput='+str(PowerOutput))
    except Exception as ex:
        pass
    try:
        NominalPower=round(Pmax*PercentPower/100)
        print('NominalPower='+str(NominalPower))
    except Exception as ex:
        pass
        
        


