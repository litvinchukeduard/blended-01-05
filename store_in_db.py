"""Consumer """
import pika

def callback(ch, method, properties, body):
    """Callback"""
    print(body)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='category_books_queue', on_message_callback=callback, auto_ack=False)
