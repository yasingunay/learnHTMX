from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from .models import Film
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from films.forms import RegisterForm

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):  # super() is a built-in function that is used to refer to the parent class
        form.save()  # save the user
        return super().form_valid(form)



# Let's break down the flow of RegisterView(FormView):

# The user accesses the URL associated with the RegisterView.
# The RegisterView renders the registration form specified by the template_name attribute ('registration/register.html').
# The user submits the registration form.
# The form_valid method is called because the form is valid.
# Inside form_valid, form.save() is called to save the user.
# After saving the user, super().form_valid(form) is called, which is the form_valid method of the parent class (FormView).
# The default behavior of FormView is to redirect to the URL specified in success_url (reverse_lazy('login')).



class FilmList (LoginRequiredMixin, ListView):
    template_name = "films.html"
    model = Film
    context_object_name = "films"

    def get_queryset(self):
       user = self.request.user
       return user.films.all()
    


def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username = username).exists():
        return HttpResponse("<div id='username-error' class='error'> This username already exists! </div>")
    else:
        return HttpResponse("<div id='username-error' class='success'> This username is available. </div>")
    

@login_required
def addFilm(request):
    name = request.POST.get("filmname")
    

    film = Film.objects.get_or_create(name=name)[0]

    # add the film to the user's list
    request.user.films.add(film)

    # return template with all of the user's film
    films = request.user.films.all()
    messages.success(request, f"Added {name} to the list of films.")
    return render(request, 'partials/film-list.html', {'films' : films})

 


@login_required
@require_http_methods(['DELETE'])
def deleteFilm(request, pk):
    user = request.user
    film = user.films.get(id = pk)
    user.films.remove(film)


    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films' : films})



  
def searchFilm(request):
    search_text = request.POST.get('search')

    userfilms = request.user.films.all()

    results = Film.objects.filter(name__icontains = search_text).exclude(
        name__in = userfilms.values_list('name', flat=True) #The flat=True option ensures that you get a flat list rather than a list of tuples.
    )

    context = {
        'results' : results
    }

    return render(request,'partials/search-results.html', context) 


def clear(request):
    return HttpResponse("")