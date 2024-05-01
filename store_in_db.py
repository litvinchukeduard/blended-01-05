"""Consumer """
import pika
import json

from mongoengine import connect
from models import Book, Category

# mongodb+srv://<username>:<password>@krabaton.5mlpr.gcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
# mongo_connection = connect(host="mongodb+srv://root:example@127.0.0.1:27017/books")
mongo_connection = connect('books',
                            host="localhost",
                            username="root",
                            password="example")


def callback(ch, method, properties, body):
    """Callback"""
    print('Received message from queue')
    books_dict = json.loads(body.decode('utf-8'))
    category_name = list(books_dict.keys())[0]

    category = Category(name=category_name)
    category.save()

    for book_name in books_dict.get(category_name):
        Book(title=book_name, category=category).save()

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='category_books_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

