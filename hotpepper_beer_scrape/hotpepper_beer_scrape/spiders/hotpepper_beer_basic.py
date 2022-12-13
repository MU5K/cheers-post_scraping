import scrapy


class HotpepperBeerBasicSpider(scrapy.Spider):
    name = 'hotpepper_beer_basic'
    allowed_domains = ['www.hotpepper.jp/SA23/Y315/lst/']
    start_urls = ['http://www.hotpepper.jp/SA23/Y315/lst//']

    def parse(self, response):
        pass
