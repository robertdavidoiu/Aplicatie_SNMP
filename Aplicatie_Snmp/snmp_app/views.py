from django.shortcuts import render
from django.http import HttpResponse


# Create your views here

posts = [
    {
        'author': 'Robert Davidoiu',
        'title': 'First post countent',
        'date_posted': '27 February 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'First post 2',
        'date_posted': '28 February 2020'
    }
]


def home(request):
    context = {
    'posts': posts
    }
    return render(request, 'snmp_app/home.html', context)

def about(request):
    return render(request, 'snmp_app/about.html', {'title': 'About'})
