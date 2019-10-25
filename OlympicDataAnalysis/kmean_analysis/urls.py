from django.contrib import admin
from django.urls import path,include
from .views import initialize,perform

urlpatterns = [
  path('init/',initialize),
  path('perform/',perform),
]