import scrapy


class TabelogBeerBasicSpider(scrapy.Spider):
    name = 'tabelog_beer_basic'
    allowed_domains = ['tabelog.com/osaka/C27127/rstLst/?SrtT=rt']
    start_urls = ['http://tabelog.com/osaka/C27127/rstLst/?SrtT=rt/']

    def parse(self, response):
        pass
