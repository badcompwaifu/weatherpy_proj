from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('thanks', views.thanks, name='thanks'),
    path('contact', views.contact, name='contact'),
    path('weather', views.weather, name='weather'),
    path('randomloc', views.random_loc, name='randomloc'),
]
