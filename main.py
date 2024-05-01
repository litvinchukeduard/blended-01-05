import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pika
import json

url = "https://books.toscrape.com"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='category_books_queue', durable=True)

def get_book_categories():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return {category.text.strip() : f'{url}/{category.get("href")}' for category in soup.select(".nav-list li ul li a")}

def get_books_by_one_category(category, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    books = defaultdict(list)
    for book in soup.select(".product_pod h3 a"):
        books[category].append(book.text.strip())
    send_book_message(books)
    print('Sent a message to books queue')
    return books

def get_books_by_category(categories):
    categories_books_dict = defaultdict(list)
    for category, url in categories.items():
        categories_books_dict[category] = get_books_by_one_category(category, url)
    return categories_books_dict

def send_book_message(category_books_dict): # {'Travel': ['', '', '']}
    category_json = json.dumps(category_books_dict)
    channel.basic_publish(exchange='',
        routing_key='category_books_queue',
        body=category_json,
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))

# soup = BeautifulSoup(response.text, 'html.parser')
# soup = BeautifulSoup(response.text, 'lxml')
# categories = soup.select(".nav-list li ul li a")
# for category in categories:
#     print(category.text.strip())
#     print(f'{url}/{category.get("href")}')
# categories = {category.text.strip() : f'{url}/{category.get("href")}' for category in soup.select(".nav-list li ul li a")}
# print(categories)

if __name__ == '__main__':
    categories = get_book_categories()
    get_books_by_category(categories)
    
    # d = defaultdict(list)
    # d = dict()
    # # if 'key1' in d:
    # #     d.get('key1').append()
    # # else:
    # #     d['key1'] = ['value1']
    # d['key1'].append('value')
    # print(d)
connection.close()
