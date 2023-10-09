import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from katalog.models import Book, AppUser
from django.contrib.auth.models import User
from katalog.views import search_book

# Create your views here.
# page=int page keberapa
def show_main(request, page_num):
    context = {}
    print("page num:",type(page_num), page_num)
    
    if request.user:
        context['name'] = request.user.username
        context['books'] = get_katalog(page_num)
        context['page_num'] = page_num

    return render(request, "main.html", context)

'''
Show main jika search
'''
def show_main_search(request):
    context = {}

    # print(request.GET.get("search_bar"))
    to_find = request.GET.get("search_bar")
    page_num =1

    if request.user:
        if 'last_searched' in request.session:
            if to_find.lower() in request.session['last_searched'].keys():
                return HttpResponse(request.session['last_searched'][to_find.lower()])
        else:
            request.session['last_searched']={}

        
        context['name'] = request.user.username
        context['books'] = search_katalog(to_find, page_num)
        context['page_num'] = page_num

        dic = request.session['last_searched']
        dic[to_find.lower()] = context['books']

    return render(request, "main.html", context)


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main", kwargs={'page_num':1}))
            response.set_cookie('last_login', str(datetime.datetime.now()), max_age=10000)
            messages.success(request, 'Hello ' + user.username + "!")
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def get_katalog(page_num):
    result=[]
    books = Book.objects.all()
    for i in range (page_num*100-100, page_num*100):
        result+=[books[i]]
        
    return result

'''
membuat daftar yang dicari
'''

def search_katalog(to_find ,page_num):
    result=[]
    books = list(search_book(to_find))
    i=page_num*100-100
    while(i<len(books) and i<page_num*100):
        result+=[books[i]]
        i+=1
        
    return result

def book_review(request, id):
    book = Book.objects.get(pk=id)
    return HttpResponse(book, content_type="text/plain")