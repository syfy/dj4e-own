from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'cats'
urlpatterns = [
    path('breed/create/', views.BreedCreate.as_view(), name='breed_create'),
    path('breed/', views.BreedView.as_view(), name='breed_view'),
    path('breed/<int:pk>/delete/', views.BreedDelete.as_view(), name='breed_delete'),
    path('breed/<int:pk>/update/', views.BreedUpdate.as_view(), name='breed_update'),

    path('', views.MainView.as_view(), name='all'),
    path('<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('create/', views.CatCreate.as_view(), name='cat_create'),
    path('<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),


    ]

