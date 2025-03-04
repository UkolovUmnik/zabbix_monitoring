import importlib
import os
import sys
import time
import logging
from zabbix import get_zabbix_keys_dict,send_to_zabbix,get_settings_zabbix
from threading import Thread

logging.basicConfig(level=logging.INFO, filename="log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")


def get_local_host(path):
    function_name='get_local_host'
    try:
        if os.path.isfile(path)==True:
            with open(path, 'r') as file:
                local_host=file.readline().strip()
                return local_host
    except Exception as e:
        logging.warning('function '+function_name)
        logging.warning(e)
        return None

def send_data(zabbix,zabbix_settings_all,metrics_to_zabbix):
    zabbix_settings=zabbix_settings_all.get(zabbix)
    if zabbix_settings!=None:
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


def get_list_modules(path):
    list_modules=[]
    with open(path, mode='r', encoding='utf-8') as file:
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
    return list_modules

def get_metrics_to_send(zabbix_list,zabbix_metrics_prev):
    zabbix_metrics_end=[]
    for zabbix_name in zabbix_list:
        zabbix_metrics_end=[]
        for zabbix_name_,metrics in zabbix_metrics_prev:
            if zabbix_name_==zabbix_name:
                for metric in metrics:
                    zabbix_metrics_end.append(metric)
    return zabbix_metrics_end


if __name__ == '__main__':
    function_name='main'

    #получаем путь настроек и имя узла
    local_host=get_local_host(r'C:\\Users\\Public\\monitoring_settings\\host.txt')

    if local_host==None:
        print('Не найден файл с именем узла по пути '+ r'C:\\Users\\Public\\monitoring_settings\\host.txt')
        logging.warning('function '+function_name)
        logging.warning('Не найден файл с именем узла по пути '+ r'C:\\Users\\Public\\monitoring_settings\\host.txt')
        input()
        sys.exit()
    logging.info('function '+function_name)
    logging.info("Получил название локального узла")    

    scripts_directory=os.path.abspath(os.curdir)
    path_to_settings=scripts_directory[0:scripts_directory.rfind('\\')]+'\\'+local_host

    list_modules=get_list_modules(scripts_directory+'\\modules.txt')
    while True:

        zabbix_list=[]
        zabbix_metrics_prev=[]

        try:
            zabbix_keys_dict=get_zabbix_keys_dict(scripts_directory)
        except Exception as e:
            logging.warning('function '+function_name)
            logging.warning('Не удалось получить ключ для Zabbix')
            print('Не удалось получить ключ для Zabbix')
            print(e)
            input()
            sys.exit()

        try:            
            zabbix_settings_all=get_settings_zabbix()
        except Exception as e:
            print('Проблема с получением настроек zabbix')
            logging.warning('function '+function_name)
            logging.warning('Проблема с получением настроек zabbix')
            print(e)
            input()
            sys.exit()

        for module in list_modules:
            try:
                thread=Thread(target=get_metrics_from_module, args=(module,zabbix_keys_dict,path_to_settings,scripts_directory,local_host), daemon=True)
                thread.start()
                thread.join()
            except Exception as e:
                logging.warning('function '+function_name)
                logging.warning('Проблема с потоком для модуля '+str(module))
                print(e)

        try:
            zabbix_metrics_end=get_metrics_to_send(zabbix_list,zabbix_metrics_prev)
            for zabbix_name in zabbix_list:
                send_data(zabbix_name,zabbix_settings_all,zabbix_metrics_end)

            print('Отправил данные')

        except Exception as e:
            print('Проблема со сборкой всех метрик и отправкой')
            logging.warning('function '+function_name)
            logging.warning('Проблема со сборкой всех метрик и отправкой')
            print (e)    


        time.sleep(45)
