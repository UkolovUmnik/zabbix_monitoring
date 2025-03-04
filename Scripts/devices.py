from os import system
import time
import os, sys
import subprocess
import traceback
from zabbix import data_to_metrics

def get_settings_for_devices(local_host,path_to_settings):
    dict_settings_for_device=dict()
    dict_change_values_for_device=dict()
    dict_change_values_for_device_all=dict()
    list_settings_for_device_all=[]
    host=''
    mode_settings=''
    #по каждому узлу получаем настройки (ip, имя в забиксе и т.д.)
    try:
        with open(path_to_settings+'\\'+local_host+'_settings_devices.txt', 'r') as file_device_settings:
            for line in file_device_settings:
                if line.startswith('#') or line.startswith('-'):
                    if dict_settings_for_device!={}:
                        list_settings_for_device_all.append({host:dict_settings_for_device})
                    if dict_change_values_for_device!={}:
                        dict_change_values_for_device_all[host]=dict_change_values_for_device
                    dict_change_values_for_device={}
                    dict_settings_for_device={}
                    
                elif line!='' and line!='\n':
                    line=line.strip().split('|')
                    if line[0]=='HOST':
                        host=line[1]
                    elif line[0]=='SETTINGS_DEVICE' or line[0]=='CHANGE_VALUES':
                        mode_settings=line[0]
                    else:
                        if mode_settings=='SETTINGS_DEVICE':
                            if line[1]!='' and line[1]!='\n':
                                dict_settings_for_device[line[0]]=line[1]
                        if mode_settings=='CHANGE_VALUES':
                            if line[1]!='' and line[1]!='\n':
                                dict_change_values_for_device[line[0]]=line[1]

        return  list_settings_for_device_all, dict_change_values_for_device_all
    except Exception as ex:
        print('Проблема с чтением настроек')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return None

def get_OID_result (OID, Community, Target, Port):
    result=''
    try:
        parametr_status=False
        result=subprocess.check_output(['SnmpGet.exe', '-r:'+Target, '-o:'+OID], text=True).split('\n')
        for element in result:
            if element=='':
                 pass
            else:
                if element.find('Value')!=-1:
                    result=element.split('=')[1]
                    parametr_status=True
                    #print(result)
    except Exception as ex:
        print('Проблема с OID')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
    if parametr_status==False:
        return ''
    else:
        return result

def get_dicts_for_WEB_and_OID_parameres(scripts_directory,settings_for_devices_list):
    dict_OID=dict()
    list_dicts_OID_commands=[]
    list_dicts_web_files=[]
    #по версии открываем файл и считываем команды или алгоритмы
    try:
        for settings_for_device_dict in settings_for_devices_list:
            for host,settings in settings_for_device_dict.items():
                mode_device=settings.get('MODE')
                version_device=settings.get('VERSION')
                if mode_device=='OID':
                    file_with_OID=scripts_directory+'\\'+'OID_commands\\OID'+'_'+version_device+'.txt'
                    if os.path.isfile(file_with_OID)==True:
                        with open(file_with_OID, 'r') as file_OID_commands:
                            for line in file_OID_commands:
                                if line!='' and line!='\n':
                                    line=line.strip().split(':')
                                    dict_OID[line[0]]=line[1]
                        list_dicts_web_files.append({})
                        list_dicts_OID_commands.append({host:dict_OID})
                elif mode_device=='WEB':
                    list_dicts_OID_commands.append({})
                    list_dicts_web_files.append({host:scripts_directory+'\\'+'web_algorithms\\WEB'+'_'+version_device+'.py'})
        return list_dicts_OID_commands,list_dicts_web_files
    except Exception as ex:
        print('Проблема с заполннием словарей WEB и OID')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return None


def change_values_in_dict(parametres_and_values_dict,change_values_dict):
    if change_values_dict==None:
        return parametres_and_values_dict  
    parametres_and_values_dict_new=dict()
    try:
        for parametr,value in parametres_and_values_dict.items():
            if value!='':
                change_value=change_values_dict.get(parametr)
                if change_value==None:
                    parametres_and_values_dict_new[parametr]=value
                else:
                    parametres_and_values_dict_new[parametr]=round(float(value)*float(change_values_dict.get(parametr)))
        return parametres_and_values_dict_new
    except Exception as ex:
        print('Проблема с изменением значений')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return None    

#def get_data_from_devices(zabbix_keys_dict):
def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
    
##    list_devices_for_monitoring=get_local_hosts(path_to_settings)
##    print(list_devices_for_monitoring)

    #на будущее словарь изменений значений нужно переделать в список, как это сделано для настроек устройств, чтобы если несколько раз задано одно и то же устройство
    #не было замены данных
    settings_for_devices_list,change_values_dict=get_settings_for_devices(local_host,path_to_settings)
    if settings_for_devices_list==[]:
        return None
    #print(settings_for_devices_list)
##    print(settings_for_devices_dict)
##    print(change_values_dict)

    list_dicts_OID_commands,list_dicts_web_files=get_dicts_for_WEB_and_OID_parameres(scripts_directory,settings_for_devices_list)
##    print(dict_OID_commands)
##    print(dict_WEB_files)

    zabbix_names=dict()
    zabbix_names_list=[]
    list_metrics_for_divices=[]
    metrics_for_divices_end=[]

    metrics_to_send_dict=dict()
    parametres_and_values_dict=dict()
    for settings_for_device_dict, dict_OID_commands, dict_WEB_files in zip(settings_for_devices_list,list_dicts_OID_commands,list_dicts_web_files):
        #print(settings_for_device_dict)
##        print(dict_OID_commands)
##        print(dict_WEB_files)
        for host_device,device_settings in settings_for_device_dict.items():
            #print(host_device)
            #spisok_for_metrics=[]
            type_device=device_settings.get('TYPE')
            mode_device=device_settings.get('MODE')
            if mode_device=='OID':
                for parametr,OID_command in dict_OID_commands.get(host_device).items():
                    result=get_OID_result(OID_command,'public',device_settings.get('IP'), 161)
                    try:
                        parametres_and_values_dict[parametr]=float(result)
                    except:
                        parametres_and_values_dict[parametr]=result
            elif mode_device=='WEB':
                result=subprocess.check_output([sys.executable, dict_WEB_files.get(host_device), device_settings.get('IP')], text=True).split('\n')
                for line in result:
                    if line!='' and line!='\n':
                        line=line.strip().split('=')
                        parametres_and_values_dict[line[0]]=line[1]
            #print(parametres_and_values_dict)
            #доп обработка
            parametres_and_values_dict=change_values_in_dict(parametres_and_values_dict,change_values_dict.get(host_device))
            #print(parametres_and_values_dict)
            metrics=[]
            for parametr,value in parametres_and_values_dict.items():
                metrics.append(data_to_metrics(host_device,parametr,value,zabbix_keys_dict))

            zabbix=device_settings.get('ZABBIX')
            if zabbix_names.get(zabbix)==None:
                zabbix_names[zabbix]=''
            zabbix_names_list.append(zabbix)
            list_metrics_for_divices.append(metrics)
                
        for zabbix_name,value in zabbix_names.items():
            metrics_for_divices_end=[]
            #print(zabbix_name)
            for zabbix,metrics in zip(zabbix_names_list,list_metrics_for_divices):
                for metric in metrics:
                    if zabbix==zabbix_name:
                        #записываем метрики всех устройств для одного zabbix
                        metrics_for_divices_end.append(metric)
                metrics_to_send_dict[zabbix]=metrics_for_divices_end
        #print(metrics_to_send_dict)
                        
    return metrics_to_send_dict
                    
