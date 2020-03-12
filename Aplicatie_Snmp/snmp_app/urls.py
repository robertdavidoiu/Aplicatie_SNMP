from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, DeviceCreateView
from .views import DeviceDetailView, DeviceDeleteView, DeviceUpdateView, DeviceListView

from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='snmp_home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('about/', views.about, name='snmp_about'),
    path('device/add/', DeviceCreateView.as_view(), name='device_create'),
    path('dashboard/', DeviceListView.as_view(), name='dashboard_view'),

    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('device/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),
    path('device/<int:pk>/update/', DeviceUpdateView.as_view(), name='device_update'),
    path('interfaces/', views.interfaces, name='device_interfaces'),
]

# <app>/<model>_<viewtype>.html
