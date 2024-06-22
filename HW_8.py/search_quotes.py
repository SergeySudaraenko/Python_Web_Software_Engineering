from mongoengine import connect
from models.author import Author
from models.quote import Quote


connect(host='mongodb+srv://<Goituser>:<567234>@cluster0.ekxs7ce.mongodb.net')


def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[-1].strip()
        author = Author.objects(fullname__icontains=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
        else:
            return []
    elif query.startswith('tag:'):
        tag = query.split(':')[-1].strip()
        quotes = Quote.objects(tags__icontains=tag)
        return quotes
    elif query.startswith('tags:'):
        tags = query.split(':')[-1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes
    else:
        return []

def main():
    while True:
        command = input("Enter command (name:<author_name>, tag:<tag>, tags:<tag1,tag2>, exit): ")
        if command == 'exit':
            break
        quotes = search_quotes(command)
        for quote in quotes:
            print(f"Author: {quote.author.fullname}")
            print(f"Quote: {quote.quote}")
            print(f"Tags: {', '.join(quote.tags)}")
            print()

if __name__ == "__main__":
    main()
