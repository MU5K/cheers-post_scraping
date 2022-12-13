import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
from retty_beer_scrape.items import RestaurantItem
from scrapy.loader import ItemLoader
from lxml import html
from bs4 import BeautifulSoup

class RettyBeerCrawlSpider(CrawlSpider):
    name = 'retty_beer_crawl'
    allowed_domains = ['retty.me']
    start_urls = ['https://retty.me/restaurant-search/search-result/?area_id=89']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//section/a[@class="restaurant__block-link"]')),
        Rule(LinkExtractor(allow=('menu/')), callback='parse_item', follow=False),
        # Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'))
    )

    def parse_item(self, response):
        logging.info(response.url)

        loader = ItemLoader(item=RestaurantItem(), response=response)
        loader.add_xpath('restaurant_name', '//h1[@class="restaurant-summary__display-name"]/text()')
        # loader.add_xpath('restaurant_address', '//p[@class="rstinfo-table__address"]/descendant::node()/text()')
        # loader.add_xpath('restaurant_tel', '//th[contains(text(),"予約・")]/following-sibling::node()/p/strong[@class="rstinfo-table__tel-num"]/text()')
        # loader.add_xpath('restaurant_url', '//li[@class="rstdtl-navi__sublist-item is-selected"]/a/@href')
        # loader.add_value('drink_name', drink_names)
        # loader.add_value('drink_price', drink_prices)
        # loader.add_xpath('drink_price', '//div[@class="rstdtl-menu-lst__info-inner"]/p[2]/text()')

        yield loader.load_item()
