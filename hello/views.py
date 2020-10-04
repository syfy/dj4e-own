from django.shortcuts import render
def index(LoginRequiredMixin,request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4 : del(request.session['num_visits'])

    context = {'num_visits': num_visits}
    response = render(request, 'hello/hello.html',context)

    response.set_cookie('dj4e_cookie', '41f860e3', max_age=1000)
    response.set_cookie('num_visits', num_visits, max_age=1000)

    return response
# Create your views here.
