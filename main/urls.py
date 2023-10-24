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
    path('book/<int:id>/', book_review , name="book_review"),
    path('profile/', show_self_profile , name="profile"),

    path('add-like/', add_like_ajax , name="add_like_ajax"),
    path('see-like/', see_like_ajax , name="see_like_ajax"),
    path('like-dislike/', like_dislike_ajax , name="like_dislike"),
    path('update-profile/',update_profile , name="update_profile"),
    path('get-username/',get_username , name="get_username"),
]