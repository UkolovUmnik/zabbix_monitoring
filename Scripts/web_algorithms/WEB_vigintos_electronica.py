from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
import time
import os
import sys
from sys import argv
                                                 
ip_transmitter=argv[1]

work_directory=os.path.abspath(os.curdir)
            
options = Options()
options.page_load_strategy = 'normal'
options.add_argument('headless')
s=Service(work_directory+'\\web_algorithms\\'+'pyatigorsk_dacha_chromedriver.exe')
driver = webdriver.Chrome(service=s,options=options)
#http://username:password@example.com/
try:
    driver.get("http://admin:1234567@"+ip_transmitter)
    time.sleep(2)
except:
    print('0')
    exit
try:
    driver.get("http://"+ip_transmitter)
    element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
except:
    print('0')
    exit
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[2]/div').click()
WebDriverWait(driver, 10)

try:        
    PowerOutput=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]').text.split(' ')[0]
    print('PowerOutput='+str(PowerOutput))
except Exception as ex:
    print('0')

try:
    RefectPower=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[2]').text.split(' ')[0]
    print('RefectPower='+str(RefectPower))
except Exception as ex:
    print('0')

try:
    Temperature=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[7]/div[2]').text.split(' ')[0]
    print('Temperature='+str(Temperature))
except Exception as ex:
    print('0')

try:
    Modulation=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[8]/div[2]').text.split(' ')[0]
    print('Modulation='+str(Modulation))
except Exception as ex:
    print('0')
    
driver.quit()


    

#driver.quit()

