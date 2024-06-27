
BOT_NAME = 'quotes_scraper'

SPIDER_MODULES = ['quotes_scraper.spiders']
NEWSPIDER_MODULE = 'quotes_scraper.spiders'

ITEM_PIPELINES = {
    'quotes_scraper.pipelines.QuotesScraperPipeline': 300,
}

ROBOTSTXT_OBEY = True


