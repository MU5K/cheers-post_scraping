import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
from hotpepper_beer_scrape.items import RestaurantItem
from scrapy.loader import ItemLoader

class HotpepperBeerCrawlSpider(CrawlSpider):
    name = 'hotpepper_beer_crawl'
    allowed_domains = ['www.hotpepper.jp']
    start_urls = ['https://www.hotpepper.jp/SA23/Y300/lst']

    rules = (
        # リンクを辿ってパースする。`follow`は、リンク先ページで同じ`XPATH`があった場合にリンクを辿ってしまうため`False`に設定する必要がある
        Rule(LinkExtractor(restrict_xpaths='//h3[contains(@class, "shopDetailStoreName")]/a'), callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=('drink/')), callback='parse_item', follow=False), # 初期のトライ
        #TODO 検索結果の2ページ目以降の取得
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pageLinkLinearBasic cf"]/li/a[contains(text(), "次へ")]'))
    )

    def parse_item(self, response):
        logging.info(response.url)
        loader = ItemLoader(item=RestaurantItem(), response=response)
        loader.add_xpath('restaurant_name', '//th[contains(text(), "店名")]/following-sibling::td[1]/text()')
        loader.add_xpath('restaurant_address', '//th[contains(text(), "住所")]/following-sibling::td[1]/address/text()')
        loader.add_xpath('restaurant_tel', '//th[contains(text(), "電話")]/following-sibling::td[1]/div/div[@class="qualificationTel"]/span/text()')
        loader.add_xpath('restaurant_url', '//div[@class="shopInfoMailContents"]/a/@href')
        drink_page = response.xpath('//div[@class="globalNav"]/ul[@class="globalNavList"]/li[@class="jscShopNavTab"]/div/ul/li/a[contains(text(), "ドリンク")]/@href').get()
        # href を urljoin() で絶対パスに変換
        drink_page = scrapy.Request(url=response.urljoin(drink_page), callback=self.parse_item_detail, meta={'item': loader.load_item()})
        yield drink_page

    def parse_item_detail(self, response):
        logging.info(response.url)
        loadernext = ItemLoader(item=response.meta['item'], response=response)
        loadernext.add_xpath('drink_name', '//div[@class="dish"]/div[@class="locator"]/div/div/div/div/h4/text()')
        loadernext.add_xpath('drink_price', '//div[@class="dish"]/div[@class="locator"]/div/div/div/div/p/text()')

        yield loadernext.load_item()


######################################################################
##### 動くやつ 別バージョン
######################################################################
    # def parse_item(self, response):
    #     item = RestaurantItem()
    #     item['restaurant_name'] = response.xpath('//th[contains(text(), "店名")]/following-sibling::td[1]/text()').get()
    #     item['restaurant_address'] = response.xpath('//th[contains(text(), "住所")]/following-sibling::td[1]/address/text()').get()
    #     item['restaurant_tel'] = response.xpath('//th[contains(text(), "電話")]/following-sibling::td[1]/div/div[@class="qualificationTel"]/span/text()').get()
    #     drink_page = response.xpath('//div[@class="globalNav"]/ul[@class="globalNavList"]/li[@class="jscShopNavTab"]/div/ul/li/a[contains(text(), "ドリンク")]/@href').get()
    #     # href を urljoin() で絶対パスに変換
    #     yield scrapy.Request(url=response.urljoin(drink_page), callback=self.parse_item_detail, meta={'item': item})

    # def parse_item_detail(self, response):
    #     item = response.meta['item']
    #     item['drink_name'] = response.xpath('//div[@class="dish"]/div[@class="locator"]/div/div/div/div/h4/text()').getall()
    #     item['drink_price'] = response.xpath('//div[@class="dish"]/div[@class="locator"]/div/div/div/div/p/text()').getall()
    #     item['restaurant_url'] = response.xpath('//div[@class="shopInfoMailContents"]/a/@href').get()
    #     return item
