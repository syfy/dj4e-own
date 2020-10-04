from django.urls import path

from . import views

app_name = 'crud'
urlpatterns = [

   #path('', views.index, name='index'),
   #path('cats', views.cats, name='cats'),
    path('', views.MainView.as_view(), name='all'),

    ]

