import pika
import mongoengine as me
from HW_8_2.models import Contact

# Підключення до MongoDB
me.connect('contacts_db')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

def send_email(contact):
    print(f"Sending email to {contact.full_name} at {contact.email}")
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for email messages. To exit press CTRL+C')
channel.start_consuming()

