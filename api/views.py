from django.shortcuts import render
from .models import RestOpening , Resturant
from rest_framework.decorators import api_view
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import re
from .serializers import RestOpeningSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q ,F 


# Create your views here.
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

def parse_datetime(my_date , my_time ):
    # get day_idx
    try:
        int(my_date[0])
        my_day_idx = str(datetime.strptime(my_date , "%Y-%M-%d").weekday() )
    except :
        day_map = ('mon', 'tue' , 'wed' , 'thu' , 'fri' , 'sat' , 'sun')
        my_day_idx  = day_map.index(my_date[:3].lower())
    
    # get time and check if it's am/pm format
    my_time = my_time.lower().replace(" ", "")
    if not re.search('m' ,my_time ):
        # This should 24-format
        data = my_time.split(':')
        hour = f"{int(data[0]):02d}"
        minutes = f"{int(data[1]):02d}"
        q_time = datetime.strptime( (':').join([hour , minutes]), '%H:%M').time()

    else:
        q_time = process_time(my_time)
    return my_day_idx ,q_time

def get_unique(ordered_dicts ):
    keys = dict()
    for i, value in enumerate(ordered_dicts):
        keys[value['Name']] = i
        
    idxs = keys.values()
    return  [ordered_dicts[i] for i in idxs]

@csrf_exempt
@api_view(["GET"])
def get_available_resturants(request):
    q_day , q_time = parse_datetime(request.query_params['date'] , request.query_params['time'])
    query_set = RestOpening.objects.filter(day= q_day, st_time__lte =q_time , end_time__gt=q_time)
    list_1 = RestOpening.objects.filter(Q(st_time__lte=F('end_time')), Q(st_time__lte=q_time), end_time__gte=q_time)
    list_2 = RestOpening.objects.filter(Q(st_time__gt=F('end_time')), Q(st_time__lte=q_time) | Q(end_time__gte=q_time))

    concat_list = (list_1 | list_2)
    print(type(concat_list))
    serlized = RestOpeningSerializer(concat_list , many = True)
    print(serlized.data[0]['Name'])
    return Response(get_unique(serlized.data) , status = status.HTTP_200_OK)


# class GetResturants(APIView):

#     @csrf_exempt
#     def get(self, request):
#         q_day , q_time = parse_datetime(request.query_params['date'] , request.query_params['time'])
#         query_set = RestOpening.objects.filter(day= q_day, st_time__lte =q_time , end_time__gte=q_time)
#         list_1 = RestOpening.objects.filter(Q(st_time__lte=F('end_time')), Q(st_time__lte=q_time), end_time__gte=q_time)
#         list_2 = RestOpening.objects.filter(Q(st_time__gt=F('end_time')), Q(st_time__lte=q_time) | Q(end_time__gte=q_time))

#         concat_list = list_1 | list_2
#         serlized = RestOpeningSerializer(concat_list , many = True)
#         return Response(serlized.data , status = status.HTTP_200_OK)
