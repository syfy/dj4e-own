from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView
app_name='myarts'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='all'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/create',
    views.ArticleCreateView.as_view(success_url=reverse_lazy('myarts:all')), name='article_create'),
    path('article/<int:pk>/update',
    views.ArticleUpdateView.as_view(success_url=reverse_lazy('myarts:all')), name='article_update'),
    path('article/<int:pk>/delete',
    views.ArticleDeleteView.as_view(success_url=reverse_lazy('myarts:all')), name='article_delete'),
]