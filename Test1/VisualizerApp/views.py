from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'VisualizerApp/index.html',
        {
            'first' : "maleikum assalam",
            'second' : "zcvzvzcxvczxv"
        }
    )

def app(request):
    return render(
        request,
       'VisualizerApp/app.html',
       {}
    )