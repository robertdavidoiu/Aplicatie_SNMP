from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='snmp_home'),
    path('about/', views.about, name='snmp_about')
]
