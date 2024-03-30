
from django.urls import path
from . import views

urlpatterns = [
    path('', views.question, name='index'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

]
