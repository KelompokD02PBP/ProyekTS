from api.views import *
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
]