import psutil
import os
import sys
import time
from os.path import getmtime
from datetime import datetime, timedelta
from zabbix import data_to_metrics

weekdays={
   1:'Пн',
   2:'Вт',
   3:'Ср',
   4:'Чт',
   5:'Пт',
   6:'Сб',
   7:'Вс',
   }


def status_files_weather(path_to_files):
   errors_list=[]
   tomorrow_date_and_time=datetime.now()+timedelta(days=1)
   tomorrow_weekday=weekdays.get(tomorrow_date_and_time.isoweekday())

   files_weather=os.listdir(path_to_files)
   for filename in files_weather:
      if filename.find('_'+tomorrow_weekday+'_')!=-1:
         if filename.split('.')[0][-1:]!='_':
            date_changing=datetime.fromtimestamp(getmtime(path_to_files+'\\'+filename))
            if (tomorrow_date_and_time-timedelta(days=2))>date_changing:
               errors_list.append(False)
   if len(errors_list)>0:
      return 0
   else:
      return 1


def get_settings_from_file(file):
   settings_weather_check_dict={}
   with open(file, encoding='utf-8', mode='r') as f:
      for line in f:
         if line.startswith('#'):
            continue
         else:
            line=line.strip().split('|')
            if line[0]=='ZABBIX':
               zabbix=line[1]
            elif line[0]=='HOST':
               host=line[1]
            elif line[0]=='PATH':
               settings_weather_check_dict[host]={'path':line[1]}
   return zabbix,settings_weather_check_dict


def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
   zabbix,settings_weather_check_dict=get_settings_from_file(path_to_settings+'\\'+local_host+'_path_weather_files.txt')
   metrics_to_zabbix=dict()
   metrics=[]
   for host,settings in settings_weather_check_dict.items():
      metrics.append(data_to_metrics(host, 'Pogoda_Status', status_files_weather(settings.get('path')), zabbix_keys_dict))
   metrics_to_zabbix[zabbix]=metrics
##   print(metrics)
   
   return metrics_to_zabbix

            



