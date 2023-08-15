from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('demo/',views.demo , name="demo"),
    path('visual/',views.visual,name="visual"),
]