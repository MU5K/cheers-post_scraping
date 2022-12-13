import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HotpepperBeerCrawlSpider(CrawlSpider):
    name = 'hotpepper_beer_crawl'
    allowed_domains = ['www.hotpepper.jp/SA23/Y315/lst/']
    start_urls = ['http://www.hotpepper.jp/SA23/Y315/lst//']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
