from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView
app_name='aads'
urlpatterns = [
    path('', views.AdListView.as_view(), name='all'),
    path('<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('create',views.AdCreateView.as_view(success_url=reverse_lazy('aads:all')), name='ad_create'),
    path('<int:pk>/update',views.AdUpdateView.as_view(success_url=reverse_lazy('aads:all')), name='ad_update'),
    path('<int:pk>/delete',
    views.AdDeleteView.as_view(success_url=reverse_lazy('aads:all')), name='ad_delete'),
]