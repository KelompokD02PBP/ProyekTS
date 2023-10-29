from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_landing, name='show_landing'),
    path('<int:page_num>/', show_main_page, name='show_main_page'),
    path('search/<int:page_num>/', show_main_search, name='show_main_search'),
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('book/<int:id>/', book_review , name="book_review"),
    # path('my-profile/', show_self_profile , name="my_profile"),
    path('profile/<int:user_id>', show_profile , name="profile"),
    
    path('add-like/', add_like_ajax , name="add_like_ajax"),
    path('see-like/', see_like_ajax , name="see_like_ajax"),
    path('like-dislike/', like_dislike_ajax , name="like_dislike"),
    path('update-profile/',update_profile , name="update_profile"),
    path('get-username/',get_username , name="get_username"),
    path('sort_books_search/<int:page_num>/<str:order_by>/',sort_books_ajax_search,name="sort_books_search"),
    path('ajax/<int:page_num>/',sort_main_ajax,name="sort_main_ajax"),
    path('ajaxsearch/<int:page_num>/',sort_main_ajax_search,name="sort_main_ajax_search"),

    path('comment/',add_comment_ajax , name="add_comment"),
    path('get-comment/',get_comments_ajax , name="get_comments_ajax"),
    path('randombookapi/', get_random_book_ajax, name="get_random_book_ajax"),

    path('get-liked-books/', get_liked_books_ajax, name="get_liked_books"),
]
