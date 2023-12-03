from django.test import TestCase, Client, AsyncClient, RequestFactory, tag
from django.contrib.auth.models import User, AnonymousUser
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile

from asgiref.sync import sync_to_async

from katalog.models import Book
from main.views import *
from main.models import *
from proyekts.settings import BASE_DIR

import json, os
from io import BytesIO
from random import choice, choices
from string import ascii_lowercase, digits
rand_chars = ascii_lowercase + digits

# Create your tests here.
class MainTest(TestCase):
    def setUp(self):
        # request factory for instant views request access
        self.factory = RequestFactory()
        
        # users (admin and non-admin)
        self.admin = User.objects.create_user(
            username="admin",
            password="top_secret",
            is_superuser=True
        )
        ProfileUser.objects.create(user=self.admin)
        self.admin_client = Client()
        self.admin_client.login(username="admin", password="top_secret")
        self.admin_async_client = AsyncClient()
        self.admin_async_client.login(username="admin", password="top_secret")

        self.user = User.objects.create_user(
            username="pakbepe",
            password="PusilkomUI",
            is_superuser=False
        )
        ProfileUser.objects.create(user=self.user)
        self.user_client = Client()
        self.user_client.login(username="pakbepe", password="PusilkomUI")
        self.user_async_client = AsyncClient()
        self.user_async_client.login(username="pakbepe", password="PusilkomUI")
    
    
    # Test random book api
    async def test_get_random_book_ajax(self):
        # fetch api
        response = await self.async_client.get(
            "/randombookapi/",
            headers={"accept": "application/json"}
        )

        # assert status_code and json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        
        # verify data model
        data = json.loads(response.content)[0]
        # print(data)
        self.assertEqual(data["model"], "katalog.book")

        # verify data fields
        fields = ["isbn", "title", "author", "year_of_publish", "publisher", "image_url_s" , "image_url_m", "image_url_l"]
        get_book = await Book.objects.aget(pk=data["pk"])
        for f in fields:
            self.assertEqual(data["fields"][f], getattr(get_book, f, None))

    # Test like system api
    async def test_like_book(self):
        # random book id
        target_book_id = choice(await sync_to_async(list)(Book.objects.all())).pk
        
        # Post user like to server
        response = await self.user_async_client.post(
            "/add-like/",
            {"id":target_book_id}
        )
        # check status_code
        self.assertEqual(response.status_code, 201)

        # Get like from server
        response = await self.user_async_client.post(
            "/see-like/",
            {"id":target_book_id}
        )
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # verify like data
        data = json.loads(response.content)[0]
        #print(data)
        self.assertEqual(data["model"], "main.like")
        self.assertEqual(data["fields"]["user"], self.user.pk)
        self.assertEqual(data["fields"]["book"], target_book_id)


        # Check admin not yet liked
        response = await self.admin_async_client.post(
            "/like-dislike/",
            {"id":target_book_id}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data)


        # Like no.2 from admin user
        # Post like to server
        response = await self.admin_async_client.post(
            "/add-like/",
            {"id":target_book_id}
        )
        # check status_code
        self.assertEqual(response.status_code, 201)

        # Get like from server
        response = await self.admin_async_client.post(
            "/see-like/",
            {"id":target_book_id}
        )
        # Check response
        self.assertEqual(response.status_code, 200)

        # verify like data
        data = json.loads(response.content)
        # print(data)
        for d in data:
            self.assertEqual(d["model"], "main.like")
            self.assertEqual(d["fields"]["book"], target_book_id)
            if d["pk"] == 2:
                self.assertEqual(d["fields"]["user"], self.admin.pk)

    # test get username api
    def test_get_username_ajax(self):
        request = self.factory.post(
            "get-username/",
            {"id": self.user.pk}
        )
        
        response = get_username(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data)
        self.assertEqual(data[0]["fields"]["username"], self.user.username)

    # Test get likes per user + profile html
    async def test_user_multiple_books_liked(self):
        # pick 5 random book ids
        target_book_ids = [i.pk for i in choices(await sync_to_async(list)(Book.objects.all()), k=5)]
        target_id_set = set(target_book_ids)

        # Post user like to server
        for idx in target_id_set:
            response = await self.user_async_client.post(
                "/add-like/",
                {"id": idx}
            )
            # check status_code
            self.assertEqual(response.status_code, 201)
        
        # Get user likes
        response = await self.user_async_client.post("/get-liked-books/")
        # check status_code
        self.assertEqual(response.status_code, 200)
        # print(response.content)
        
        # data success
        data = json.loads(response.content)
        # print(data)
        self.assertEqual(data["status"], "success")

        # check likes
        retrived_like_id = set()
        retrived_books = json.loads(data["books"])
        for book in retrived_books:
            retrived_like_id.add(book["pk"])
        
        self.assertEqual(retrived_like_id, target_id_set)
        
        # Get user profile
        response = await self.user_async_client.get("/profile/"+str(self.user.pk))
        # check status_code
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

        books_you_liked = set()
        for like in response.context["books_you_like"]:
            books_you_liked.add(like.book.pk)
        self.assertEqual(books_you_liked, target_id_set)

    # Test profile updating api
    def test_update_profile(self):
        # Create new user
        user = User.objects.create_user(
            username="testacc",
            password="testinggrounds",
            is_superuser=False
        )
        ProfileUser.objects.create(user=user)

        img = None
        with open(os.path.join(BASE_DIR, "testdata/pakbepe.jpg"), "rb") as fp:
            img = SimpleUploadedFile("pakbepe.jpg", fp.read(), content_type="image/jpg")

        request = self.factory.post(
            "/update-profile/",
            {
                "id": user.pk,
                "Username": "changedname",
                "Address": "something",
                "Email": "test@website.com",
                "profile_picture": img,
            }
        )
        
        request.user = user
        response = update_profile(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)[0]
        self.assertNotEqual(User.objects.get(pk=user.pk).username, "testacc")

    # Test comment system api
    async def test_comment_system(self):
        # random book id
        target_book_id = choice(await sync_to_async(list)(Book.objects.all())).pk
        # secret
        secret = ''.join(choices(rand_chars, k=8))

        # Post 2 user comments to server
        response = await self.user_async_client.post(
            "/comment/",
            {
                "id":target_book_id,
                "comment":"This is a test comment. " + secret,
            }
        )
        self.assertEqual(response.status_code, 201) # check status_code
        response = await self.user_async_client.post(
            "/comment/",
            {
                "id":target_book_id,
                "comment":"This is another test comment. " + secret,
            }
        )
        self.assertEqual(response.status_code, 201) # check status_code

        # Get book comments
        response = await self.user_async_client.post(
            "/get-comment/",
            {"id":target_book_id}
        )
        # Check response
        self.assertEqual(response.status_code, 200)

        # verify comment data
        data = json.loads(response.content)
        # print(data)
        for comment in data:
            self.assertEqual(comment["model"], "main.comment")
            self.assertEqual(comment["fields"]["user"], self.user.pk)
            self.assertIn(secret, comment["fields"]["comment"])   
    
    # Test sorting of books api
    async def test_book_sorting(self):
        # sort yearly ascending
        response = await self.user_async_client.post(
            "/ajax/1/",{"order_by": 3}
        )
        self.assertEqual(response.status_code, 200) # check status_code
        self.assertEqual(response.headers["Content-Type"], "application/json")
        data = json.loads(response.content)
        # print(data)
        year = -100000
        for book in data:
            self.assertGreaterEqual(book["fields"]["year_of_publish"], year)
            year = book["fields"]["year_of_publish"]

        # sort name ascending
        response = await self.user_async_client.post(
            "/ajax/1/",{"order_by": 1}
        )
        self.assertEqual(response.status_code, 200) # check status_code
        self.assertEqual(response.headers["Content-Type"], "application/json")
        data = json.loads(response.content)
        # print(data)
        prev = ""
        for book in data:
            self.assertGreaterEqual(book["fields"]["title"], prev)
            prev = book["fields"]["title"]

    # Test book search
    def test_book_search(self):
        response = self.user_client.get(
            '/search/1', 
            {
                "order_by": "asc",
                "search_bar": "the"
            },
            follow=True
        )
        # basic
        self.assertEqual(response.status_code, 200) # check status_code
        self.assertTemplateUsed(response, 'main.html')
        # print(response)

        # test search
        books = response.context["books"]
        for book in books:
            self.assertIn("the".casefold(), book.title.casefold())


        # ajax search, no async
        
        response = self.user_client.post(
            '/ajaxsearch/2/', 
            {
                "order_by": "asc",
            }
        )
        # basic
        self.assertEqual(response.status_code, 200) # check status_code
        self.assertEqual(response.headers["Content-Type"], "application/json")
        print(response)

        # test search
        data = json.loads(response.content)
        for book in data:
            self.assertIn("the".casefold(), book["fields"]["title"].casefold())
    
    

    # =======================
    # Template tests
    # =======================

    def test_landing_page_template(self):
        response = self.user_client.get('/')
        self.assertTemplateUsed(response, 'landing.html')

    def test_book_page_template(self):
        target_book_id = choice(Book.objects.all()).pk
        response = self.user_client.get('/book/'+str(target_book_id)+'/')
        # print(response)

        self.assertEqual(response.context["book"].pk, target_book_id)
        self.assertTemplateUsed(response, 'book.html')

    def test_main_page_template(self):
        response = self.user_client.get(
            '/1', 
            {"order_by": 1},
            follow=True
        )
        self.assertTemplateUsed(response, 'main.html')
