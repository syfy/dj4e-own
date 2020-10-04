from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from crud.models import Auto, Make
class MainView( View):
    def get(self, request):
        mc = Make.objects.all().count()
        al = Auto.objects.all()

        ctx = {'make_count': mc, 'auto_list': al}
        return render(request, 'autos/auto_list.html', ctx)


@login_required
def index(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4 : del(request.session['num_visits'])

    context = {'num_visits': num_visits}
    response = render(request, 'hello/hello.html',context)

    response.set_cookie('dj4e_cookie', '41f860e3', max_age=1000)
    response.set_cookie('num_visits', num_visits, max_age=1000)

    return response
# Create your views here.

def cats(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4 : del(request.session['num_visits'])

    context = {'num_visits': num_visits}
    response = render(request, 'hello/hello.html',context)

    response.set_cookie('dj4e_cookie', '41f860e3', max_age=1000)
    response.set_cookie('num_visits', num_visits, max_age=1000)

    return response

