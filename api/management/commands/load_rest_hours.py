from django.core.management import BaseCommand
from api.models import Resturant , RestOpening
import pandas as pd
from datetime import datetime
import re
import time 
# Python program to convert time 
# from 12 hour to 24 hour format 

# Function to convert the date format 
# Python program to convert time 
# from 12 hour to 24 hour format 

# Function to convert the date format 
def convert24(str1): 
	# Checking if last two elements of time 
	# is AM and first two elements are 12 
	if str1[-2:] == "AM" and str1[:2] == "12": 
		return "00" + str1[2:-2] 
		
	# remove the AM	 
	elif str1[-2:] == "AM": 
		return str1[:-2] 
	
	# Checking if last two elements of time 
	# is PM and first two elements are 12 
	elif str1[-2:] == "PM" and str1[:2] == "12": 
		return str1[:-2] 
		
	else: 
		
		# add 12 to hours and remove PM 
		return str(int(str1[:2]) + 12) + str1[2:5] 

# Driver Code		 


def process_time(t_str):
    t_str = t_str.lower().replace(" " ,"")
    pm_index = t_str.index('m')
    pm_str = t_str[pm_index-1:pm_index+1].upper()
    data = t_str[:pm_index-1].split(':')
    if len(data) == 1 :
        hour = f"{int(data[0]):02d}"
        minutes = '00'
    else:
        hour = f"{int(data[0]):02d}"
        minutes = f"{int(data[1]):02d}"
        
    time_str = convert24(((':').join([hour, minutes]))+pm_str)
    time_object = datetime.strptime(time_str, '%H:%M').time()
    return time_object
           

def process_time_str(t_str):
    times = t_str.split('-')
    return [process_time(t) for t in times]

def find(str, ch):
    idx_list =[]
    for i, ltr in enumerate(str):
        if ltr == ch:
            idx_list.append(i)
    return idx_list

def process_days_str(d_str):
    day_map = ('mon', 'tue' , 'wed' , 'thu' , 'fri' , 'sat' , 'sun')
    d_str = d_str.lower().replace(" " ,"")
    # Get index of ',' and '-'
    comma_idxs = find(d_str , ',')
    dash_idxs = find(d_str , '-')
    # this function can divied to async funcs for faster run-time
    day_list = []
    for com_idx in comma_idxs:
        day = d_str[com_idx+1:com_idx+4]
        day_list.append(day)
        
    for dash_idx in dash_idxs:
        first_day = d_str[dash_idx-3:dash_idx]
        last_day = d_str[dash_idx+1 :dash_idx+4]
        day_list.append(last_day)
        day_idx = day_map.index(last_day)
        curr_idx = day_map.index(first_day)
        curr_day = first_day
        while(curr_idx != day_idx):
                day_list.append(curr_day)
                curr_idx = (curr_idx+1) % 7
                curr_day = day_map[curr_idx]
    if len(comma_idxs) == len(dash_idxs) == 0:
        day = d_str[:3]
        day_list.append(day)
    return [str(day_map.index(day)) for day in day_list]

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--filename' , type=str)

    def handle(self , *args , **kwargs):
        filename = kwargs['filename']
        df = pd.read_csv('rest_hours.csv' ,header=None, names= ['rest_name' , 'rest_opening'])
        # insert into resturnant table 
        model_instances = [Resturant(name=record['rest_name']) for record in df.to_dict('rest_name')]
        Resturant.objects.bulk_create(model_instances)

        # Insert opening times
        for idx  ,row  in df.iterrows():
            data = row['rest_opening'].split('/')
            rest_id = Resturant.objects.filter(name=row['rest_name'] )[0]
            for d_str in data:
                d_str  = d_str.strip()
                num_idx = re.search("\d" , d_str).start()
                if not num_idx:
                    # Do something
                    continue
                days_list = process_days_str(d_str[:num_idx] )
                st_time , end_time = process_time_str(d_str[num_idx:])
                model_instances = [RestOpening(rest_id = rest_id , day = day , st_time = st_time , end_time =end_time) for day in days_list]
                RestOpening.objects.bulk_create(model_instances)
                # print(model_instances)

