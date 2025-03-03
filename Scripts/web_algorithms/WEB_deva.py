from sys import argv
import time
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
session=requests.session()
login='admin'
password='root'
url='http://'+ip_transmitter+'/basic.ssi?idx=5952'
page=session.get(url=url, auth=(login, password))
page.encoding="windows-1252"
soup = str(BeautifulSoup(page.text, 'html.parser'))
#print(soup)

dict_ = eval(soup)
#print(dict_.get("outL"))

OUT_L_list=dict_.get("outL")
Left_level_sound1=round(OUT_L_list[0]*80/20480)
print('LevelSound='+str(Left_level_sound1))
'''    
    Left_level_sound1=OUT_L_list[1]
    if Left_level_sound1<-7000:
        print('Left_level_sound2')
        print(Left_level_sound2)
    Left_level_sound1=OUT_L_list[2]
    if Left_level_sound1<-7000:
        print('Left_level_sound3')
        print(Left_level_sound3)
'''
    
