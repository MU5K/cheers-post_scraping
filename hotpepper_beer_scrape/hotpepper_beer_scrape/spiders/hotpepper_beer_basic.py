import scrapy


class HotpepperBeerBasicSpider(scrapy.Spider):
    name = 'hotpepper_beer_basic'
    allowed_domains = ['www.hotpepper.jp']
    start_urls = ['https://www.hotpepper.jp/SA23/Y300/lst']

    def parse(self, response):
        restaurants = response.xpath('//h3[contains(@class, "shopDetailStoreName")]/a')

        for restaurant in restaurants:
            yield {
                'name': restaurant.xpath('.//text()').get(),
                'URL': restaurant.xpath('.//@href').get()
            }
            # yield response.follow(url=restaurant.xpath('.//@href').get(), callback=self.parse_item)

        # 次のページへ移動して取得
        next_page = response.xpath('//ul[@class="pageLinkLinearBasic cf"]/li/a[contains(text(), "次へ")]/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    # def parse_item(self, response):
    #     yield {
    #         'restaurant_name': response.xpath('//th[contains(text(), "店名")]/following-sibling::td[1]/text()').get(),
    #         'restaurant_address': response.xpath('//th[contains(text(), "住所")]/following-sibling::td[1]/address/text()').getall()
    #     }
