from sys import argv
import requests
from bs4 import BeautifulSoup

ip_transmitter=argv[1]
try:
    html=requests.get('http://'+ip_transmitter+'/')
    html.encoding="windows-1251"
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print (message)
    exit
else:
    #print('Забрал страницу')

    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find("table", align="center")
    output = []
    for row in table.findAll("tr"):
        new_row = []
        for cell in row.findAll(["td"]):
            new_row.append(cell.get_text().strip())
        output.append(new_row)
    rez = []
    for i in range(len(output)):
        bebra = " ".join(output[i][0:4])
        rez.append(bebra)

    rez.remove("   ")

    begin=int(rez[0].find("=")+1)
    end=int(rez[0].find("Вт")-1)
    PowerOutput=float(rez[0][begin:end])
                
    print('PowerOutput='+str(PowerOutput))
                
    begin=int(rez[1].find("=")+1)
    end=int(rez[1].find("Вт")-1)
    PowerReflect=float(rez[1][begin:end])
                
    print('PowerReflect='+str(PowerReflect))
                
    begin=int(rez[4].find("=")+1)
    end=int(rez[4].find("кГц")-1)
    Modulation=float(rez[4][begin:end])

    print('Modulation='+str(Modulation))
            
    begin=int(rez[3].find("=")+1)
    end=int(rez[3].find("С")-1)
    Temperature=float(rez[3][begin:end])

    print('Temperature='+str(Temperature))
