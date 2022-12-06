import scrapy


class TabelogBeerBasicSpider(scrapy.Spider):
    name = 'tabelog_beer_basic'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/osaka/C27127/rstLst/?SrtT=rt']

    def parse(self, response):
        restaurants = response.xpath('//h3/a[@class="list-rst__rst-name-target cpy-rst-name js-ranking-num"]')

        for restaurant in restaurants:
            yield {
                'name': restaurant.xpath('.//text()').get(),
                'URL': restaurant.xpath('.//@href').get()
            }

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
