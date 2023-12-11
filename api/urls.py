from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
]