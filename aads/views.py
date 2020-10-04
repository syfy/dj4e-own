from django.shortcuts import render
from aads.owner import OwnerListView,OwnerCreateView,OwnerDetailView,OwnerUpdateView,OwnerDeleteView
# Create your views here.
#AdListView

from aads.models import Ad

class AdListView(OwnerListView):
    model = Ad
    # By convention:
    # template_name = "myarts/article_list.html"

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'text','price']

class AdDetailView(OwnerDetailView):
    model = Ad



class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'text','price']


class AdDeleteView(OwnerDeleteView):
    model = Ad