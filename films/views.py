from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model

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



def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username = username).exists:
        return HttpResponse("This username already exists!")
    else:
        return HttpResponse("This username is available.")