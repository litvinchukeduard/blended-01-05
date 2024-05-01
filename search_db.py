from mongoengine import connect
from models import Category, Book

import redis
from redis_lru import RedisLRU

client = redis.Redis(host='localhost', port=6379, password="my-password")
cache = RedisLRU(client)

mongo_connection = connect('books',
                            host="localhost",
                            username="root",
                            password="example")

@cache
def get_books_by_category(category_name: str):
    category = Category.objects(name=category_name).first()
    if category:
        books = Book.objects(category=category).all()
        return books
    return []


while True:
    category_name = input('Enter category name: ')
    if category_name == 'quit':
        break
    for book in get_books_by_category(category_name):
        print(book.title)
