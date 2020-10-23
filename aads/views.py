from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from aads.owner import OwnerListView,OwnerCreateView,OwnerDetailView,OwnerUpdateView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from aads.forms import CreateForm,CommentForm
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.
#AdListView

from aads.models import Ad,Comment,Fav
from django.db.models import Q
class AdListView(OwnerListView):
    model = Ad
    # By convention:
    template_name = "aads/ad_list.html"
    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval:
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
            favorites = list()
            if request.user.is_authenticated:
                # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
                rows = request.user.favorite_ads.values('id')
                # favorites = [2, 4, ...] using list comprehension
                favorites = [ row['id'] for row in rows ]
            ctx = {'ad_list' : ad_list, 'favorites': favorites, 'search': strval}

        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]
            favorites = list()
            if request.user.is_authenticated:
                # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
                rows = request.user.favorite_ads.values('id')
                # favorites = [2, 4, ...] using list comprehension
                favorites = [ row['id'] for row in rows ]
            ctx = {'ad_list' : ad_list, 'favorites': favorites, 'search': strval}

        return render(request, self.template_name, ctx)

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
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

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


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('aads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "aads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('aads:ad_detail', args=[ad.id])


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        a = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=a)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        a = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=a).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()