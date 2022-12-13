import scrapy


class RettyBeerBasicSpider(scrapy.Spider):
    name = 'retty_beer_basic'
    allowed_domains = ['retty.me']
    start_urls = ['https://https://retty.me/restaurant-search/search-result/?area_id=89']

    def parse(self, response):
        pass
