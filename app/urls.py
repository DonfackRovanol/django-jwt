
from django.urls import path
from .views import *


urlpatterns =[
    path('', home, name='home'),
    path('register', register, name='register'),
    path('login', logIn, name='login'),
    path('logout', lOgout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]