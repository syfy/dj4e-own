from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from cats.forms import BreedForm
# Create your views here.
from cats.models import Cat,Breed
from django.urls import reverse_lazy

class MainView(LoginRequiredMixin,View):
    def get(self, request):
        mc = Breed.objects.all().count()
        al = Cat.objects.all()

        ctx = {'breed_count': mc, 'cat_list': al}
        return render(request, 'cats/cat_list.html', ctx)


class BreedCreate(LoginRequiredMixin,View):
    template = 'cats/breed_form.html'
    success_url = reverse_lazy('cats:breed_view')

    def get(self, request):
        form = BreedForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = BreedForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        make = form.save()
        return redirect(self.success_url)

class CatCreate(LoginRequiredMixin,CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')
class CatDelete(DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')
class CatUpdate(LoginRequiredMixin,UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedView(LoginRequiredMixin,View):
    def get(self, request):
        al = Breed.objects.all()

        ctx = {'breed_list': al}
        return render(request, 'cats/breed_list.html', ctx)
class BreedUpdate(LoginRequiredMixin,UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_view')
class BreedDelete(LoginRequiredMixin,DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_view')