
import requests
from bs4 import BeautifulSoup
from .models import Author, Quote, Tag

def scrape_quotes():
    url = 'http://quotes.toscrape.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote_block in soup.select('.quote'):
        text = quote_block.select_one('.text').get_text()
        author_name = quote_block.select_one('.author').get_text()
        tags = [tag.get_text() for tag in quote_block.select('.tag')]

        author, created = Author.objects.get_or_create(name=author_name)
        quote = Quote.objects.create(text=text, author=author)

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)
