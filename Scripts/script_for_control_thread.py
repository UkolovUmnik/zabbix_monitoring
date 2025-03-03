from os import system
import importlib
##try:
##    import psutil
##except:
##    system("pip install psutil")
##    import psutil
import os
import sys
import time
import subprocess
from zabbix import get_zabbix_keys_dict,send_to_zabbix,get_settings_zabbix
#from multiprocessing import Process
from threading import Thread


zabbix_list=[]
zabbix_metrics_prev=[]
##
##import inspect
##
##try:
##    import bad_module
##except Exception, e:
##    frm = inspect.trace()[-1]
##    mod = inspect.getmodule(frm[0])
##    modname = mod.__name__ if mod else frm[1]
##    print 'Thrown from', modname

def get_local_host(path):
    try:
        if os.path.isfile(path)==True:
            with open(path, 'r') as file:
                local_host=file.readline().strip()
                return local_host
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return None



def send_data(zabbix,zabbix_settings_all,metrics_to_zabbix):
    #print(metrics_to_zabbix)
    zabbix_settings=zabbix_settings_all.get(zabbix)
    if zabbix_settings!=None:
    #print(zabbix_settings)
        return send_to_zabbix(zabbix_settings.get('zabbix_server'),int(zabbix_settings.get('zabbix_port')),int(zabbix_settings.get('timeout')),metrics_to_zabbix)
    return None
    
def get_metrics_from_module(module,zabbix_keys_dict,path_to_settings,scripts_directory,local_host):
    global zabbix_metrics_prev
    importlib.reload(module)
    metrics_to_zabbix=module.main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host) #{zabbix_name:[metrics]}
                        
    if metrics_to_zabbix!=None and metrics_to_zabbix!={}:           
        for zabbix,metrics in metrics_to_zabbix.items():
            if zabbix not in zabbix_list:
                zabbix_list.append(zabbix)
            zabbix_metrics_prev.append((zabbix,metrics))


if __name__ == '__main__':
    #получаем путь настроек и имя узла
    local_host=get_local_host(r'C:\Users\Public\monitoring_settings\host.txt')
    print(local_host)
    if local_host==None:
        print('Не найден файл с именем узла по пути '+ r'C:\Users\Public\monitoring_settings\host.txt')
        input()
        sys.exit()
       
    scripts_directory=os.path.abspath(os.curdir)
    path_to_settings=scripts_directory[0:scripts_directory.rfind('\\')]+'\\'+local_host

    list_modules=[]
    with open(scripts_directory+'\\modules.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                name_module=line.strip()
                try:
                    module = importlib.import_module(name_module)
                    list_modules.append(module)
                    print('Импортировал модуль '+name_module)
                except Exception as ex:
                    print('Проблема с модулем '+name_module)
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print (message)

    while True:

        zabbix_list=[]
        zabbix_metrics_prev=[]

        try:
            #загрузка ключей для забикса
            zabbix_keys_dict=get_zabbix_keys_dict(scripts_directory)
        except Exception as ex:
            print('Проблема со словарем ключей zabbix')
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)

        try:            
            #получаем настройки забиксов
            zabbix_settings_all=get_settings_zabbix()
            #print(zabbix_settings_all)
        except Exception as ex:
            print('Проблема с получением настроек zabbix')
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)

        for module in list_modules:
            try:
                thread=Thread(target=get_metrics_from_module, args=(module,zabbix_keys_dict,path_to_settings,scripts_directory,local_host), daemon=True)
                thread.start()
                thread.join()
            except Exception as ex:
                print('Проблема с модулем '+name_module)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)

        try:
            for zabbix_name in zabbix_list:
                zabbix_metrics_end=[]
                for zabbix_name_,metrics in zabbix_metrics_prev:
                    if zabbix_name_==zabbix_name:
                        for metric in metrics:
                            zabbix_metrics_end.append(metric)
                send_data(zabbix_name,zabbix_settings_all,zabbix_metrics_end)

            print('Отправил данные')

        except Exception as ex:
            print('проблема со сборкой всех метрик и отправкой')
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)    


        time.sleep(45)
