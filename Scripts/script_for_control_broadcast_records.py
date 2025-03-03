from datetime import datetime
import os
import time
import locale
import json
from zabbix import data_to_metrics
import SELogger
import RadioLogger
import common_parts

def get_month_name(num):
   lang_encoding=int(locale.getlocale()[1])
   en = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
          'october', 'november', 'december']
   ru = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
          'октябрь', 'ноябрь', 'декабрь']
   if lang_encoding == 1251:
      return ru[num - 1]
   else:
      return en[num - 1]
                      
def find_files_with_need_hour(path_to_files,need_hour):
    result=[]
    for root, dirs, files in os.walk(path_to_files):
        for filename in files:
            if filename.startswith(need_hour):
                result.append(filename)
    return result

def get_parametres_record_programs(programs_file):
   result=[]
   result_prev=[]
   with open(programs_file, 'r', encoding='utf-8') as programs_settings:
      for line in programs_settings:
         if line.startswith('###'):
            if result_prev!=[]:
                  result.append((host,result_prev))  
                  result_prev=[]   
         if line.startswith('#'):
            pass
         else:
            line=line.strip().split('|')
            if line[0]=='ZABBIX':
               zabbix=line[1]
            elif line[0]=='HOST':
               host=line[1]
            elif line[0]=='Record':
               result_prev.append({'program_name':line[1],'path_broadcast_records':line[4],'path_config_program':line[5]})        
   return zabbix,result


def get_full_path_records(path_to_records,current_datetime):
   path_to_files_records=None
   current_day=str(current_datetime.day)
   if len(current_day)==1:
      current_day='0'+current_day
   if os.path.exists(path_to_records+'\\'+str(current_datetime.year)+'\\'+str(current_datetime.month))==True:
      path_to_files_records=path_to_records+'\\'+str(current_datetime.year)+'\\'+str(current_datetime.month)+'\\'+current_day      
   else:
      name_of_month=get_month_name(current_datetime.month)
      if os.path.exists(path_to_records+'\\'+str(current_datetime.year)+'\\'+name_of_month)==True:
         path_to_files_records=path_to_records+'\\'+str(current_datetime.year)+'\\'+name_of_month+'\\'+current_day
   return path_to_files_records
   

def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
##   print(path_to_settings)
   info_last_files=r'C:\Users\Public\monitoring_settings\last_files_broadcast_records.txt'
   programs_file = path_to_settings+'\\'+local_host+'_programs_for_control_hovering.txt'
##   print(programs_file)

   if os.path.isfile(programs_file)==False:
      print(programs_file)
      print('файл с параметрами программ отсутствует')      
      return None

   zabbix,all_settings_record_programs=get_parametres_record_programs(programs_file)

   checks_false=[]
   checks_false_at_all=[]

   if os.path.isfile(info_last_files):
      with open(info_last_files, mode='r', encoding='utf-8') as file:
         for line in file:
            line=line.strip().split('|')
            if line[0]=='names_last_file':
               names_last_file=json.loads(line[1].replace("'",'"'))
            if line[0]=='sizes_last_file':
               sizes_last_file=json.loads(line[1].replace("'",'"'))
   else:
      names_last_file={}
      sizes_last_file={}        


   current_datetime = datetime.now()
   need_hour=str(current_datetime.hour)
   current_day=str(current_datetime.day)
   number_weekday=current_datetime.weekday()
        
   if len(need_hour)==1:
      need_hour='0'+need_hour 

   metrics_to_zabbix=dict()
   metrics=[]
   for host, settings in all_settings_record_programs:
      for settings_record_program in settings:

         program_name=settings_record_program.get('program_name')
         if program_name=='SELogger':
            need_hours_dict=SELogger.get_need_hours_of_records_dict(settings_record_program.get('path_config_program'))
         elif program_name=='RadioLogger':
            need_hours_dict=RadioLogger.get_shedule_radiologger_dict(settings_record_program.get('path_config_program'))
         else:
            print('Неизвестная программа записи эфира: '+program_name)

         if need_hours_dict=={}:
            checks_false.append(False)
            continue
            
            
         need_hours_in_current_day=need_hours_dict.get(number_weekday)
         if int(need_hour) not in need_hours_in_current_day:           
            continue

         path_broadcast_records=settings_record_program.get('path_broadcast_records')
         full_path_to_records=get_full_path_records(path_broadcast_records,current_datetime)
         if full_path_to_records==None:
            checks_false.append(False)
            continue
              
         files_with_need_hour=find_files_with_need_hour(full_path_to_records, need_hour)
         if files_with_need_hour==[]:
            checks_false.append(False)
         else:
            name_last_file=names_last_file.get(path_broadcast_records)
            if name_last_file!=None:
               if name_last_file==files_with_need_hour[len(files_with_need_hour)-1]:
                  size_of_last_file=sizes_last_file.get(path_broadcast_records)
                  if size_of_last_file!=None:
                     if size_of_last_file==os.stat(full_path_to_records+'\\'+files_with_need_hour[len(files_with_need_hour)-1]).st_size:
                        checks_false.append(False)

            names_last_file[path_broadcast_records]=files_with_need_hour[len(files_with_need_hour)-1]
            sizes_last_file[path_broadcast_records]=os.stat(full_path_to_records+'\\'+files_with_need_hour[len(files_with_need_hour)-1]).st_size

         if len(checks_false)!=0:
            checks_false_at_all.append(False)
      if len(checks_false_at_all)==0:
         result=1
      else:
         result=0
      metrics.append(data_to_metrics(host, 'records', result, zabbix_keys_dict))
   metrics_to_zabbix[zabbix]=metrics
   with open(info_last_files, mode='w+', encoding='utf-8') as file:
      file.write('names_last_file|'+str(names_last_file)+'\n')
      file.write('sizes_last_file|'+str(sizes_last_file)+'\n')
   return metrics_to_zabbix
            
