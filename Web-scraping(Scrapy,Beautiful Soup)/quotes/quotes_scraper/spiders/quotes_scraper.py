import scrapy
from quotes_scraper.items import QuoteItem, AuthorItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('span small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

            author_url = quote.css('span a::attr(href)').get()
            yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_item = AuthorItem()
        author_item['name'] = response.css('h3.author-title::text').get().strip()
        author_item['birthdate'] = response.css('span.author-born-date::text').get().strip()
        author_item['bio'] = response.css('div.author-description::text').get().strip()
        yield author_item

