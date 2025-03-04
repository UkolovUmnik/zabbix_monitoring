from pyzabbix import ZabbixAPI, ZabbixMetric, ZabbixSender
import socket


def data_to_metrics(host, parametr, value, zabbix_keys_dict):
    try:
        key=zabbix_keys_dict.get(parametr)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
    return ZabbixMetric(host, key, value, clock=None)

def is_conencted():
   try:
     socket.gethostbyname('www.yandex.ru')
   except socket.gaierror:
     return False
   return True

def chek_port(host,port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection
          
#получаем настройки Забикс сервера (ip-адрес, порт и время таймаута)
def get_settings_zabbix():
    zabbix_settings=dict()
    zabbix_settings_all=dict()
    with open('zabbix_settings.txt', 'r') as file_zabbix_settings:
        for line in file_zabbix_settings:
            if line.startswith('#'):
                pass
            else:
                line=line.strip().split('|')
                if line[0]=='ZABBIX':
                    if zabbix_settings!={}:
                        zabbix_settings_all[Host_zabbix]=zabbix_settings 
                    Host_zabbix=line[1]
                    zabbix_settings={}
                else:
                    if line[0]=='zabbix_server':
                        line[1]=socket.gethostbyname(line[1])
                    zabbix_settings[line[0]]=line[1]
        zabbix_settings_all[Host_zabbix]=zabbix_settings        
    return zabbix_settings_all

def get_zabbix_keys_dict(scripts_directory):           
    zabbix_keys_dict=dict()            
    #получаем настройки ключей забикса, формируем словарь
    file_to_zabbix_keys=scripts_directory+'\\'+'zabbix_keys.txt'
    with open(file_to_zabbix_keys, 'r') as zabbix_keys:
        for line in zabbix_keys:
            if line.startswith('#'):
                pass
            else:
                line=line.strip().split(':')
                zabbix_keys_dict[line[0]]=line[1]
            
    return zabbix_keys_dict
            

def send_to_zabbix(Host_zabbix,zabbix_port,timeout,metrics):
    connection_internet=is_conencted()
    if connection_internet==True:
        status_send=False
        #print('Забикс в порядке')
        if is_conencted():         
            try:
                zbx=ZabbixSender(zabbix_server=Host_zabbix, zabbix_port=zabbix_port, socket_wrapper=None, timeout=timeout)
                zbx.send(metrics)
                status_send=True
                #print('Отправил данные'+'\n')
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
                return False
        else:
            print('нет интернета')
    return status_send

                        
                



