from django.urls import path
from .views import PostListView,  DeviceCreateView
from .views import DeviceDetailView, DeviceDeleteView, DeviceUpdateView, DeviceListView, DeviceInterfaceView
from .views import interfaces
from . import views



urlpatterns = [
    path('', PostListView.as_view(), name='snmp_home'),
    path('about/', views.about, name='snmp_about'),


    path('device/add/', DeviceCreateView.as_view(), name='device_create'),
    path('dashboard/', DeviceListView.as_view(), name='dashboard_view'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('device/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),
    path('device/<int:pk>/update/', DeviceUpdateView.as_view(), name='device_update'),
    path('device/interfaces/', views.interfaces, name='device_interfaces'),
]

# <app>/<model>_<viewtype>.html
