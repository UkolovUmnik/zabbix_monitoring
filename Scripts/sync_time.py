from os import system
try:
    import ntplib
except:
    system("pip install ntplib")
    import ntplib
import os
from datetime import datetime
import time
from zabbix import data_to_metrics


def get_ntp_servers_from_file(file):
    ntp_servers=[]
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:       
            if line.startswith('#'):
                pass
            else:
                ntp_servers.append(line.strip())
    return ntp_servers

def get_settings_dict_from_file(file):
    settings_dict=dict()            
    with open(file, 'r') as f:
        for line in f:       
            if not line.startswith('#'):
                line=line.strip().split('|')
                settings_dict[line[0]]=line[1]
    return settings_dict

def get_work_ntp_server(file):
    result=None
    if os.path.isfile(file):
        with open(file, 'r') as f:
            result=f.read().strip()   
    return result

def write_work_ntp_server(file,ntp_server):
    with open(file, 'w+') as f:
        f.write(ntp_server)   

def get_date_and_time_ntp_server_str(ntp_client,ntp_server):
    try:
        response = ntp_client.request(ntp_server)
        response.offset
            
        data_and_time=time.localtime(response.tx_time)
        date_server=time.strftime('%d-%m-%Y',data_and_time)
        time_server=time.strftime('%H:%M',data_and_time)
        return date_server,time_server
    except:
##        print('Проблема с сервером '+ntp_server)
        return None,None


def find_work_ntp_server(ntp_client,ntp_servers):
    for ntp_server in ntp_servers:
        date_server,time_server=get_date_and_time_ntp_server_str(ntp_client,ntp_server)
        if date_server!=None:
            work_ntp_server=ntp_server
            break    
    return work_ntp_server


def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
    file_work_server=r'C:\Users\Public\monitoring_settings\work_ntp_server.txt'
    ntp_servers=[]
    status=0

    ntp_servers=get_ntp_servers_from_file(scripts_directory+'\\ntp-servers.txt')   
    settings_dict=get_settings_dict_from_file(path_to_settings+'\\'+local_host+'_sync_time_settings.txt')
    work_ntp_server=get_work_ntp_server(file_work_server)
    
    ntp_client = ntplib.NTPClient()
    #находим рабочий сервер (проверяем записанный, если нет, ищем новый)
    if work_ntp_server==None:    
        work_ntp_server=find_work_ntp_server(ntp_client,ntp_servers)
    else:
        date_server,time_server=get_date_and_time_ntp_server_str(ntp_client,work_ntp_server)
        if date_server==None:
            work_ntp_server=find_work_ntp_server(ntp_client,ntp_servers)

    date_server,time_server=get_date_and_time_ntp_server_str(ntp_client,work_ntp_server)
    write_work_ntp_server(file_work_server,work_ntp_server)
            
    current_date_and_time=datetime.now()
    current_date=current_date_and_time.strftime('%d-%m-%Y')
    current_time=current_date_and_time.strftime('%H:%M')

    if date_server==current_date and time_server==current_time:
        status=1

    metrics_to_zabbix=dict()
    metrics=[]
    metrics.append(data_to_metrics(settings_dict.get('HOST'), 'system_time', status, zabbix_keys_dict))
    metrics_to_zabbix[settings_dict.get('ZABBIX')]=metrics
       

    return metrics_to_zabbix
   
