import pika
import mongoengine as me
from faker import Faker
from models import Contact

# Підключення до MongoDB
me.connect('contacts_db')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

fake = Faker()

def create_contacts(n=10):
    contacts = []
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            preferred_method=fake.random_element(elements=('email', 'sms'))
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_to_queue(contacts):
    for contact in contacts:
        message = str(contact.id)
        if contact.preferred_method == 'email':
            channel.basic_publish(exchange='',
                                  routing_key='email_queue',
                                  body=message)
        else:
            channel.basic_publish(exchange='',
                                  routing_key='sms_queue',
                                  body=message)
        print(f"Sent {contact.full_name} to {contact.preferred_method} queue")

if __name__ == "__main__":
    contacts = create_contacts(10)
    send_to_queue(contacts)
    connection.close()








