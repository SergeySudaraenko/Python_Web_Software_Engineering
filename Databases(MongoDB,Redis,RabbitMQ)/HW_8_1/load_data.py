import json
from mongoengine import connect
from models.author import Author
from models.quote import Quote

uri = "mongodb+srv://Goituser:567234@cluster0.ekxs7ce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def connect_to_database():
    connect(host=uri)

def load_authors_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author_data in authors:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def load_quotes_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote_data in quotes:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(
                    author=author,
                    quote=quote_data['quote'],
                    tags=quote_data.get('tags', [])
                )
                quote.save()

def main():
    connect_to_database()  
    load_authors_from_file('authors.json')
    load_quotes_from_file('quotes.json')
    print(" Все пройшло норм.")

if __name__ == "__main__":
    main()

