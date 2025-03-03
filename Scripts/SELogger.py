import common_parts


def get_need_hours_of_records_dict(path_config):
   numbers_sum_houres_for_days=get_numbers_sum_houres_for_days(path_config)
   need_hours_in_days=dict()
   
   for i in range(0,7):
      sum_hours=numbers_sum_houres_for_days[i]
      if sum_hours==0:
         need_hours_in_days[i]=[]
      need_hours_in_day=[]
      while sum_hours>0:
         hour_of_record=common_parts.max_degree_of_2(sum_hours)
         need_hours_in_day.append(hour_of_record)
         sum_hours-=2**hour_of_record
      need_hours_in_days[i]=need_hours_in_day
   return need_hours_in_days


def get_numbers_sum_houres_for_days(path_config):
   sum_hours_day=[0,0,0,0,0,0,0]
   sum_indexes=0
   with open(path_config,'r') as settings:
         for line in settings:
            if line.startswith('DayWeek'):
               line=line.strip().split('=')
               try:
                  index_sum_hours_day=int(line[0].replace('DayWeek',''))
                  sum_indexes+=index_sum_hours_day
                  sum_hours_day[index_sum_hours_day]=int(line[1])
               except Exception as ex:
                  template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  print (message)
                        
   if sum_indexes!=21:
      return None

   return sum_hours_day
