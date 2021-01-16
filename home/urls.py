from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='Search'),
    path('signup', views.handleSignup, name='HandleSignup'),
    path('login', views.handleLogin, name='HandleLogin'),
    path('logout', views.handleLogout, name='HandleLogout'),

]