from django.urls import path 
from . import views 
from django.conf.urls import url , include
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('get_rest' , views.GetResturants )

urlpatterns = [
  path('open_rest/' , views.get_available_resturants , name='get_resturants'),
  # path('get_rest/' , views.GetResturants , name = "Get rest"),
]
