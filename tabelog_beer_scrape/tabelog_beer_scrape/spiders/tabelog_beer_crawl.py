import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
from tabelog_beer_scrape.items import RestaurantItem
from scrapy.loader import ItemLoader


class TabelogBeerCrawlSpider(CrawlSpider):
    name = 'tabelog_beer_crawl'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/osaka/C27127/rstLst/?SrtT=rt']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a[@class="list-rst__rst-name-target cpy-rst-name js-ranking-num"]')),
        Rule(LinkExtractor(allow=('dtlmenu/drink/')), callback='parse_item', follow=False),
        # Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'))
    )

    def parse_item(self, response):
        logging.info(response.url)

        loader = ItemLoader(item=RestaurantItem(), response=response)
        loader.add_xpath('restaurant_name', '//div[@class="rstinfo-table__name-wrap"]/descendant::node()/text()')
        loader.add_xpath('restaurant_address', '//p[@class="rstinfo-table__address"]/descendant::node()/text()')
        loader.add_xpath('restaurant_url', '//li[@class="rstdtl-navi__sublist-item is-selected"]/a/@href')
        loader.add_xpath('drink_menu', '//p[@class="rstdtl-menu-lst__menu-title"]/text()')
        loader.add_xpath('drink_price', '//p[@class="rstdtl-menu-lst__price"]/text()')

        yield loader.load_item()

        yield {
            'restaurant_name': response.xpath('//div[@class="rstinfo-table__name-wrap"]/descendant::node()/text()').get(),
            'restaurant_address': response.xpath('//p[@class="rstinfo-table__address"]/descendant::node()/text()').getall(),
            'restaurant_url': response.xpath('//li[@class="rstdtl-navi__sublist-item is-selected"]/a/@href').get(),
            'drink_menu': response.xpath('//p[@class="rstdtl-menu-lst__menu-title"]/text()').getall(),
            'drink_price': response.xpath('//p[@class="rstdtl-menu-lst__price"]/text()').getall()
        }
