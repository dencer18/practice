from django.urls import path
#from django.contrib.auth.views import LoginView
from myauth.views import (
    AboutMeView, 
    RegisterView,
    get_cookie_view,
    FooBarView
    )


app_name = 'myauth'

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name="about-me"),
    path('register/', RegisterView.as_view(), name="register"),
    path('cookie/get/', get_cookie_view, name="cookie-get"),
    path('boo-bar/', FooBarView.as_view(), name="foo-bar"),
      

]