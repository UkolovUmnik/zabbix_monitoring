import psutil
import os
import sys
import time
from zabbix import data_to_metrics
    
def get_programs_statuses_tuple(programs_settings_list,programs_names_for_search_dict):
    processes_list=[]
    for process in psutil.process_iter():
        try:
            processes_list.append((process.name(),process.exe()))
        except:
            pass
    programs_statuses=[]
    for program_settings_dict in programs_settings_list:
        program_name=program_settings_dict.get('program_name')
        program_name_for_search=programs_names_for_search_dict.get(program_name)
        status=0
        for process_name,process_path in processes_list:
            if process_name.startswith(program_name_for_search):
                program_path=program_settings_dict.get('program_path')
                if program_path==process_path:
                    if process.status()=='running':
                        status=1
        
        programs_statuses.append((program_name,status))
                    
    return programs_statuses        


def get_programs_settings_for_all_hosts_dict(file):
    programs_settings_for_all_hosts_dict=dict()
    programs_settings_list=[]
    with open(file, encoding='utf-8', mode='r') as f:
        for line in f:
            if line.startswith('###'):
               if programs_settings_list!=[]:
                  programs_settings_for_all_hosts_dict[host]=programs_settings_list
               programs_settings_list=[]
            elif line.startswith('#'):
                continue
            else:
                line=line.strip().split('|')
                if line[0]=='ZABBIX':
                    zabbix=line[1]
                elif line[0]=='HOST':
                   host=line[1]
                else:
                    programs_settings_list.append({'program_name':line[1],'program_path':line[3]})
    return zabbix,programs_settings_for_all_hosts_dict

def get_names_for_search_dict(file):
    programs_names_for_search_dict=dict()
    with open(file, encoding='utf-8', mode='r') as f:
        for line in f:
            if not line.startswith('#'):
                line=line.strip().split(':')
                programs_names_for_search_dict[line[0]]=line[1]
    return programs_names_for_search_dict


def main(zabbix_keys_dict,path_to_settings,scripts_directory,local_host):    
    zabbix,programs_settings_for_all_hosts_dict=get_programs_settings_for_all_hosts_dict(path_to_settings+'\\'+local_host+'_programs_for_control_hovering.txt')

    programs_names_for_search_dict=get_names_for_search_dict(scripts_directory+'\\'+'programs_names_for_search.txt')

    metrics_to_zabbix=dict()
    metrics=[]
    for host, programs_settings_list in programs_settings_for_all_hosts_dict.items():
        programs_statueses_tuple=get_programs_statuses_tuple(programs_settings_list,programs_names_for_search_dict)
        for program_name,status in programs_statueses_tuple:
            metrics.append(data_to_metrics(host, program_name, status, zabbix_keys_dict))        

    metrics_to_zabbix[zabbix]=metrics
   
    return metrics_to_zabbix
    
    



