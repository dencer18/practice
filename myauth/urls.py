from django.urls import path
#from django.contrib.auth.views import LoginView
from myauth.views import (
    AboutMeView, 
    RegisterView,
    )


app_name = 'myauth'

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name="about-me"),
    path('register/', RegisterView.as_view(), name="register"),
      

]