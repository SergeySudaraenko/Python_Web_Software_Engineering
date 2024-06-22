from mongoengine import Document, ReferenceField, ListField, StringField
from .author import Author

class Quote(Document):
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
    tags = ListField(StringField())
