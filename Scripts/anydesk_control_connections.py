import os
import codecs
from datetime import datetime
import time
from zabbix import data_to_metrics

connections_history_file=r"C:\\ProgramData\AnyDesk\\connection_trace.txt"

def delete_probels(line_elements):
    for element in line_elements:
        if element=='':
            line_elements.remove('')
            delete_probels(line_elements)

def get_settings_dict(path_to_settings,local_host):
    settings_dict=dict()
    with open(path_to_settings+'\\'+local_host+'_remote_control_check_settings.txt', encoding='windows-1251', mode='r') as file:
        for line in file:
            if not line.startswith('#'):
                line=line.strip().split('|')
                if line[1]!='' and line[1]!='\n':
                    settings_dict[line[0]]=line[1]
    return settings_dict


#дописать
def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
    settings_dict=get_settings_dict(path_to_settings,local_host)
    if settings_dict=={}:
        return None

    last_date_and_time=None            
    if os.path.isfile(r'C:\Users\Public\monitoring_settings\AD_connections_last_date.txt'):
        with open(r'C:\Users\Public\monitoring_settings\AD_connections_last_date.txt', mode='r', encoding='utf-8') as file:
            for line in file:
                if line!='' and line!='\n':
                    try:
                        last_date_and_time=datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
                    except Exception as ex:
                        print('Модуль соединений anydesk')
                        print('Не удалось получить из файла дату и время последней проверки')
                        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print (message)
        if last_date_and_time==None:
            last_date_and_time=datetime.strptime('1980-05-01 05:40', '%Y-%m-%d %H:%M')    
                
    else:
        last_date_and_time=datetime.strptime('1980-05-01 05:40', '%Y-%m-%d %H:%M')

    date_and_time=''
    AD_number='0'
    spisok_for_metrics=[]
    with open(connections_history_file, mode='rb') as file:
        for line in file:
            line=str(codecs.decode(line.replace(b'\x00', b''), 'utf-8')).strip()
            line_elements=line.split(' ')
            delete_probels(line_elements)
            if line_elements!=[]:
                type_login=line_elements[3]
                date_and_time=datetime.strptime(line_elements[1].replace(',','')+' '+line_elements[2], '%Y-%m-%d %H:%M')
                if type_login=='Passwd' and date_and_time>last_date_and_time:
                    AD_number=line_elements[4]
            
    last_date_and_time=date_and_time
    with open(r'C:\Users\Public\monitoring_settings\AD_connections_last_date.txt', mode='w+', encoding='utf-8') as file:
            file.write(str(last_date_and_time))
            
    metrics_to_zabbix=dict()
    metrics=[]
    metrics.append(data_to_metrics(settings_dict.get('HOST'),'AD_number',AD_number,zabbix_keys_dict))
    metrics_to_zabbix[settings_dict.get('ZABBIX')]=metrics

    return metrics_to_zabbix
       
