from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('',                        views.home,             name='home'),
    path('properties/add/',         views.property_add,     name='add'),
    path('properties/',             views.property_list,    name='list'),
    path('properties/<int:pk>/',    views.property_detail,  name='detail'),
    path('map/',                    views.property_map,     name='map'),
]