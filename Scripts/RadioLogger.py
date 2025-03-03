def shedule_from_radiologger_string(path_config):
    with open(path_config,mode='r',encoding='utf-8') as file:
        buf=''
        status_shedule=False
        for line in file:
            if line.startswith('    ') and status_shedule==True:
                buf+=line
            elif line.startswith('  Schedule'):
                status_shedule=True
            elif line.startswith('  ') and status_shedule==True:
                break
    return buf

def get_need_hours_dict_from_numbers_in_string(shedule_string):
    need_hours_all_days=dict()
    count_hours_in_day=24
    current_hour=0
    current_day=0
    hours_in_day=[]
    for char in shedule_string:
        if char=='1':
            hours_in_day.append(current_hour)
        if current_hour==count_hours_in_day-1:
            need_hours_all_days[current_day]=hours_in_day
            hours_in_day=[]
            current_day+=1
            current_hour=0
        current_hour+=1
    return need_hours_all_days
        

def get_shedule_radiologger_dict(path_config):    
    shedule_str=shedule_from_radiologger_string(path_config)
    shedule_str_normal=''
    for char in shedule_str:
        if char in ['0','1']:
            shedule_str_normal+=char
    return get_need_hours_dict_from_numbers_in_string(shedule_str_normal)

