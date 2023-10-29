from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory

from katalog.models import Book
from katalog.views import *
from main.models import ProfileUser

# Create your tests here.
class KatalogTest(TestCase):
    def setUp(self):
        # request factory, immediate access to functions in views
        self.factory = RequestFactory()
        
        # users (admin and non-admin)
        # self.admin = User.objects.create_user(
        #     username="admin",
        #     password="top_secret",
        #     is_superuser=True
        # )
        # ProfileUser.objects.create(user=self.admin)
        self.user = User.objects.create_user(
            username="pakbepe",
            password="top_secret",
            is_superuser=False
        )
        ProfileUser.objects.create(user=self.user)


    def test_database_loaded_and_available(self):
        # check database is not empty
        self.assertNotEqual(len(Book.objects.all()), 0)

        # get books api
        request = self.factory.get("/katalog/get-books")
        request.user = self.user

        response = get_books(request)

        # test response exists
        self.assertTrue(response.content)

    def test_search_book2(self):
        queries = ["the", "star", "is", "silent", "and", "driving", "to", "Prague"]

        # test search book works
        for s in queries:
            books = search_book2(s)
            for book in books:
                self.assertIn(s.casefold(), book.title.casefold())

        