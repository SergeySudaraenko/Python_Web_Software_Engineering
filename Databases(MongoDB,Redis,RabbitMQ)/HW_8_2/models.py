import mongoengine as me

class Contact(me.Document):
    full_name = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone_number = me.StringField(required=True)
    message_sent = me.BooleanField(default=False)
    preferred_method = me.StringField(choices=['email', 'sms'], required=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

