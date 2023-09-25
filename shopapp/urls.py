from django.urls import path
from . import views
#from shopapp.views import first_page

app_name = 'shopapp'

urlpatterns = [
    path('', views.page2, name='first_page'),    
]