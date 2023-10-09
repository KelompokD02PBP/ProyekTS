from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('<int:page_num>/', show_main_page, name='show_main_page'),
    path('search/<int:page_num>', show_main_search, name='show_main_search'),
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('book/<int:id>', book_review , name="book_review")
]