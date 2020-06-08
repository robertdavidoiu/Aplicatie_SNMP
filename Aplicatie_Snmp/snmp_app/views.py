from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Device
from django.http import HttpResponse
import datetime
from .device.snmp_data import x
from .device.snmp_data import SnmpSession
from django.shortcuts import get_object_or_404

# Create your views here


def home(request):
    context = {
    'devices': Device.objects.all()
    }
    return render(request, 'snmp_app/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'snmp_app/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 2


class DeviceListView(ListView):
    model = Device
    template_name = 'snmp_app/dashboard.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'devices'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['name', 'ip_address', 'subnet_mask', 'Snmp_Username', 'Authentication_Protocol', 'Authentication_Password',
              'Private_Protocol', 'Private_Password', 'Details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeviceDetailView(DetailView):
    model = Device


class DeviceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Device
    fields = ['name', 'ip_address', 'subnet_mask', 'Snmp_Username', 'Authentication_Protocol', 'Authentication_Password',
              'Private_Protocol', 'Private_Password', 'Details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        device = self.get_object()
        if self.request.user == device.author:
            return True
        return False


class DeviceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Device
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeviceInterfaceView(ListView):
    model = Device
   #  ce = Device()
    #ce.retrieve_interface_data()


class DeviceDataView(DetailView):
    model = Device

    def retrieve_interface_data(self):
        snmpobject = self.get_object()
        merge = SnmpSession(snmpobject.ip_address, snmpobject.name, snmpobject.Authentication_Password,
                         snmpobject.Private_Password, snmpobject.Authentication_Protocol, snmpobject.Private_Protocol)
        return merge.retrieve_interface_data()


def interfaces(request):

    snmpobject = get_object_or_404(Device, pk=8)
    merge = SnmpSession(snmpobject.ip_address, snmpobject.name, snmpobject.Authentication_Password,
                         snmpobject.Private_Password, snmpobject.Authentication_Protocol, snmpobject.Private_Protocol)

    context = {'devices': x.retrieve_interface_data(),
               'date_now': datetime.datetime.now()
               }
    return render(request, 'snmp_app/interfaces.html', context)


def deviceMonitoringStats(request):
    context = {'devices': x.retrieve_device_data(),
               'date_new': datetime.datetime.now()
               }
    return render(request, 'snmp_app/device_details.html', context)


def about(request):
    return render(request, 'snmp_app/about.html', {'title': 'About'})
