import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse

from katalog.models import Book
from django.contrib.auth.decorators import login_required
from katalog.views import search_book2
from .models import Like, ProfileUser

from .forms import ProfileUserForm

from django.core import serializers
from django.core.validators import validate_email

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000

from re import match

def show_main(request):
    context = {}
    
    if request.user:
        context['name'] = request.user.username
        context['page_num']=-1 #Kalo blm login gk bisa ngapa-ngapain
        
        context['aaa'] = request.user.pk

        if request.user.id !=None: #Kalo udh login bisa liat halaman
            context['page_num']=1
            context['likes']=get_liked_books(request.user)
            context['user_id']=request.user.pk
            context['books']=get_katalog(1,order_by=request.GET.get('order_by'))

    return render(request, "main.html", context)


def show_main_page(request, page_num):
    context = {}
    
    if request.method == 'POST':
        order_by_value = request.POST.get('order_by')
        if order_by_value == '1':
            order_by = "asc"
        elif order_by_value == '2':
            order_by = "desc"
        elif order_by_value == '3':
            order_by = "year_asc"
        elif order_by_value == '4':
            order_by = "year_desc"
        elif order_by_value == '5':
            order_by = "atas_2000"
        elif order_by_value == '6':
            order_by = "bawah_2000"
        else:
            order_by = request.GET.get('order_by', 'asc')
    else:
        order_by = request.GET.get('order_by', 'asc')

    if request.user:
        context['name'] = request.user.username
        context['books'] = get_katalog(page_num)
        context['likes']=get_liked_books(request.user)
        if page_num <= 0:
            page_num = 1
        context['books'] = get_katalog(page_num, order_by=order_by)
        context['page_num'] = page_num
        context['user_id']=request.user.pk


    return render(request, "main.html", context)

'''
Show main jika search
'''
books_last_searched=[] #simpen search sebelumnya biar bisa next/prior page dengan cepat
last_searched="" #simpen kata yang di search terakhir


def show_main_search(request, page_num):
    global books_last_searched
    global last_searched
    context = {}

    order_by  = request.GET.get('order_by')
    to_find = request.GET.get("search_bar")
    print("last_searched:",last_searched)
        
    if request.user:
        context['name'] = request.user.username
        if(page_num<=0):
            page_num=1
        context['page_num'] = page_num
        context['from_search']=True
        context['user_id']=request.user.pk

        #search string kosong
        if to_find!=None and len(to_find)==0 and last_sort_by==order_by:
            return HttpResponseRedirect(reverse("main:show_main_page", kwargs={'page_num':1}))

        # yang dicari beda lagi, kosongin list sebelumnya
        # to_find != None buat pastiin bukan gr gr refresh/nextpage
        if to_find != None and last_searched!=to_find:
            books_last_searched=[]
            last_searched=""
        
        
        # kalo blm pernah search atau search hal baru
        if len(books_last_searched)==0:
            books = search_katalog(to_find, page_num,order_by=request.GET.get('order_by'))
            context['books'] = books

        # ganti page
        else:
            books = search_katalog(last_searched, page_num,order_by=request.GET.get('order_by'))

            #Next page tapi udh habis
            if(len(books)==0):
                books = search_katalog(last_searched, page_num-1,order_by=request.GET.get('order_by'))
                context['page_num']=page_num-1
            context['books'] = books
    #   
    return render(request, "main.html", context)

def register(request):
    user_form = UserCreationForm()
    profile_form = ProfileUserForm()

    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileUserForm(request.POST or None, request.FILES or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            profile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main_page", kwargs={'page_num':1}))
            response.set_cookie('last_login', str(datetime.datetime.now()), max_age=10000)
            messages.success(request, 'Hello ' + user.username + "!")
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response


def get_katalog(page_num,order_by):
    result=[]
    books = Book.objects.all()
    
    print(order_by)
    if order_by == 'asc' or order_by==None:
        books = Book.objects.all().order_by("title")
    elif order_by =='desc':
        books = Book.objects.all().order_by("-title")
    elif order_by == "year_asc":
        books = Book.objects.all().order_by("year_of_publish")
    elif order_by == "year_desc":
        books = Book.objects.all().order_by("-year_of_publish")
    elif order_by == "atas_2000":
        books = Book.objects.filter(year_of_publish__gte=2000)
    elif order_by == "bawah_2000":
        books = Book.objects.filter(year_of_publish__lt=2000)
    i=page_num*20-20
    while(i<page_num*20 and i<len(books)):
        result+=[books[i]]
        i+=1

    return result


def get_liked_books(user) :
    likes = []
    if user:
        # Mengambil book yang telah dilike oleh user
        liked_books = Like.objects.filter(user = user).order_by('-timestamp')
        for like in liked_books: likes.append(like.book)
    
    return likes



'''
membuat daftar yang dicari
'''
last_sort_by = ""
def search_katalog(to_find ,page_num,order_by):
    global books_last_searched
    global last_searched
    global last_sort_by
    # search hal baru
    if len(books_last_searched)==0 or order_by!=last_sort_by:
        result=[]
        books = list(search_book2(to_find))
        print(type(books))
        
        if order_by=='asc' or order_by == None:
            books = list(search_book2(to_find).order_by("title"))
        elif order_by=='desc':
            books = list(search_book2(to_find).order_by("-title"))
        elif order_by == "year_asc":
            books = list(search_book2(to_find).order_by("year_of_publish"))
        elif order_by == "year_desc":
            books = list(search_book2(to_find).order_by("-year_of_publish"))
        elif order_by == "atas_2000":
            books = list(search_book2(to_find).filter(year_of_publish__gte=2000))
        elif order_by == "bawah_2000":
            books = list(search_book2(to_find).filter(year_of_publish__lt=2000))
            
        i=page_num*20-20

        books_last_searched = books
        last_searched = to_find
        last_sort_by = order_by
        while(i<len(books) and i<page_num*20):
            result.append(books[i])
            i+=1

    # ganti page
    else:
        result=[]
        books = books_last_searched
        
        i=page_num*20-20

        while(i<len(books) and i<page_num*20):
            result.append(books[i])
            i+=1

    return result


# Ke page per buku
def book_review(request, id):
    context={}
    if request.user:
        book = Book.objects.get(pk=id)
        context['book']=book
        context['name'] = request.user.username
        context['user_id'] = request.user.pk
    return render(request, 'book.html', context)

# Method buat buka profile page orang lain
def show_profile(request, user_id):
    print("in show_profile")
    print(user_id)
    profile = ProfileUser.objects.get(user__pk=user_id)
    books_you_like = Like.objects.filter(user__pk=user_id)
    print("books", profile.user.username ,"person like like", books_you_like)
    context = {"profile":profile}
    context['name']=request.user.username
    context['books_you_like']=books_you_like
    context['self_profile']=request.user==profile.user
    context['user_id']=user_id
    print(context['self_profile'])
    
    return render(request, "profile.html", context)

# Function untuk menambahakan like
@csrf_exempt
def add_like_ajax(request):
    # print("in add_like_ajax views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        book = Book.objects.get(pk=id)

        has_like = Like.objects.filter(book = book, user = request.user)
        # print("has like =",has_like)

        # print("anjing", book, request.user)
        if len(has_like)==0:
            like = Like(user = request.user,
                        book = book
                        )
            # print("like",like)
            like.save()
        else:
            has_like.delete()

        return HttpResponse(b"LIKED", status=201)
    return HttpResponseNotFound()

#Function untuk mendapatkan daftar siapa saja yang pernah like bukunya
@csrf_exempt
def see_like_ajax(request):
    # print("in add_like_ajax views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        # print("id",id)
        book = Book.objects.get(pk=id)
        likes = Like.objects.filter(book=book)
        # print("likes", type(likes))

        return HttpResponse(serializers.serialize('json',likes))
    return HttpResponseNotFound()

#Function untuk mengetahui apakah user dalam kondisi like atau tidak terhadap buku
@csrf_exempt
def like_dislike_ajax(request):
    # print("in like_dislike views.py")
    if request.method == 'POST':
        id = request.POST.get("id")
        book = Book.objects.get(pk=id)
        likes = Like.objects.filter(book=book, user = request.user)

        return HttpResponse(serializers.serialize('json',likes))
    return HttpResponseNotFound()

@csrf_exempt
def update_profile(request):
    print("in update_profile")

    if request.method == 'POST':
        address = request.POST.get("Address")
        email = request.POST.get("Email")
        image = request.FILES.get("profile_picture")
        print("img/",image)
        username = request.POST.get("Username")
        already_exist = User.objects.filter(username=username)

        user_id = request.POST.get("id")
        user = User.objects.get(pk=user_id)
        profile = ProfileUser.objects.filter(user=user)[0]

        #Jika username taken by another person
        if(len(already_exist)!=0 and already_exist[0].pk != profile.pk):
            messages.info(request, 'Sorry, username taken')
            return HttpResponse(serializers.serialize('json',[profile]), content_type="application/json")
        
        #Jika bukan email
        try:
            validate_email(email)
        except:
            messages.info(request, 'Invalid email')
            return HttpResponse(serializers.serialize('json',[profile]), content_type="application/json")
        
        # check media validity
        if image != None:
            try:
                img = Image.open(image)
                img.verify()
            except:
                messages.info(request, 'Invalid image')
                return HttpResponse(serializers.serialize('json',[profile]), content_type="application/json")

        profile.address = address
        profile.email = email
        profile.profile_picture = image
        user.username = username
        user.save()
        profile.save()

        print(profile)
        return HttpResponse(serializers.serialize('json',[profile]))
    return HttpResponseNotFound()

@csrf_exempt
def get_username(request):
    id = request.POST.get("id")
    print("id in getusername",id)
    user = User.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json',user))

def sort_books_ajax(request,page_num,order_by):
    sorted_books = get_katalog(page_num,order_by)
    return HttpResponse(serializers.serialize('json',sorted_books))

@csrf_exempt
def sort_books_ajax_search(request,page_num,order_by):
    sorted_books = search_katalog(last_searched, page_num,order_by)
    return HttpResponse(serializers.serialize('json',sorted_books))

@csrf_exempt
def sort_main_ajax(request,page_num):
    order_by=""
    if request.method == 'POST':
        order_by_value = request.POST.get('order_by')
        if order_by_value == '1':
            order_by = "asc"
        elif order_by_value == '2':
            order_by = "desc"
        elif order_by_value == '3':
            order_by = "year_asc"
        elif order_by_value == '4':
            order_by = "year_desc"
        elif order_by_value == '5':
            order_by = "atas_2000"
        elif order_by_value == '6':
            order_by = "bawah_2000"
        else:
            order_by = request.GET.get('order_by', 'asc')
    else:
        order_by = request.GET.get('order_by', 'asc')
        
    sorted_books = get_katalog(page_num,order_by)
    
    return HttpResponse(serializers.serialize('json',sorted_books))

@csrf_exempt
def sort_main_ajax_search(request,page_num):
    order_by=""
    if request.method == 'POST':
        order_by_value = request.POST.get('order_by')
        if order_by_value == '1':
            order_by = "asc"
        elif order_by_value == '2':
            order_by = "desc"
        elif order_by_value == '3':
            order_by = "year_asc"
        elif order_by_value == '4':
            order_by = "year_desc"
        elif order_by_value == '5':
            order_by = "atas_2000"
        elif order_by_value == '6':
            order_by = "bawah_2000"
        else:
            order_by = request.GET.get('order_by', 'asc')
    else:
        order_by = request.GET.get('order_by', 'asc')
        
    sorted_books = search_katalog(last_searched, page_num,order_by)
    
    return HttpResponse(serializers.serialize('json',sorted_books))