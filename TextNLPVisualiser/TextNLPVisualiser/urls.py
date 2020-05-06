"""
Definition of urls for TextNLPVisualiser.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('segmentation/', views.segmentation, name='segmentation' ),
    path('tokenization/', views.tokenization, name='tokenization' ),
    path('tagger/', views.tagger, name='tagger' ),
    path('chunk/', views.chunk, name='chunk' ),
    path('application/', views.application, name='application' ),
    path('application/process', views.process, name='process' ),
]
