from django.contrib import admin
from django.urls import path, include
from .views import process_form
urlpatterns = [
    path('', process_form, name='help_me'),
    ]