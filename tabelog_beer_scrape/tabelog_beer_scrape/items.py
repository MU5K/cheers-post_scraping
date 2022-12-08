# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantItem(scrapy.Item):
    restaurant_name = scrapy.Field()
    restaurant_address = scrapy.Field()
    restaurant_tel = scrapy.Field()
    restaurant_url = scrapy.Field()
    drink_menu = scrapy.Field()
    # drink_price = scrapy.Field()
