from django.db import migrations
from proyekts.settings import BASE_DIR
import os
import time
import csv


def generate_database(apps, schema_editor):
    Book = apps.get_model("katalog", "Book")
    db_alias = schema_editor.connection.alias
    
    source= os.path.join(BASE_DIR, 'datasets/Books.csv')
    print("\nall books test:")

    tm = time.time()

    book_list = []
    with open(os.path.join(source, 'Books.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            book = Book(
                isbn = row['ISBN'],
                title = row["Book-Title"].replace("\n", " ").replace("\r"," "),
                author = row["Book-Author"],
                # subject = row["Subjects"]
                year_of_publish = row['Year-Of-Publication'],
                publisher = row['Publisher'],
                image_url_s = row['Image-URL-S'],
                image_url_m = row['Image-URL-M'],
                image_url_l = row['Image-URL-L']
            )
            book_list.append(book)
    
    print(f"csv took {time.time() - tm} seconds")
    tm = time.time()

    Book.objects.using(db_alias).bulk_create(book_list)

    print(f"django took {time.time() - tm} seconds")

def delete_database(apps, schema_editor):
    Book = apps.get_model("katalog", "Book")
    books = Book.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("katalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(generate_database, delete_database),
    ]