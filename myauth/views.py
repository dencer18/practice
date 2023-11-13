from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# class MyLogoutView(LogoutView):
#     next_page=reverse_lazy("accounts:login")

class AboutMeView(TemplateView):
    template_name="myauth/about_me.html"

class RegisterView(CreateView):
    form_class=UserCreationForm
    template_name='myauth/register.html'
    success_url=reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        responce = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password, 
        )
        login(request=self.request, user=user)
        return responce

def set_cookie_view(request: HttpRequest)->HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest)->HttpResponse:
    value = request.COOKIES.get("fizz", "default")
    return HttpResponse(f"Cookie value: {value!r}")

def set_session_view(request: HttpRequest)->HttpResponse:
    request.session["foobar"]="spameggs"
    return HttpResponse("Session set!")

def get_session_view(request: HttpRequest)->HttpResponse:
    value = request.session.get("foobar","default")
    return HttpResponse(f"Session value: {value!r}")