from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from aads.owner import OwnerListView,OwnerCreateView,OwnerDetailView,OwnerUpdateView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from aads.forms import CreateForm
from django.http import HttpResponse
# Create your views here.
#AdListView

from aads.models import Ad

class AdListView(OwnerListView):
    model = Ad
    # By convention:
    template_name = "aads/ad_list.html"

class AdCreateView(LoginRequiredMixin, View):
    model = Ad
   # fields = ['title', 'text','price']
    template_name = 'aads/ad_form.html'
    success_url = reverse_lazy('aads:all')
    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "aads/ad_detail.html"


class AdUpdateView(LoginRequiredMixin, View):
    model = Ad
    template_name = 'aads/ad_form.html'
    success_url = reverse_lazy('aads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)



class AdDeleteView(OwnerDeleteView):
    model = Ad


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response