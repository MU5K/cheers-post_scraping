# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

# def strip_yen(element):
#     if element is None:
#         return ""
#     return element.replace("円", "")

# def strip_comma(element):
#     if element:
#         return element.replace(",", "")
#     return element

# def strip_integer(element):
#     if element:
#         return int(element)
#     return 0


class RestaurantItem(scrapy.Item):
    restaurant_name = scrapy.Field(
        # output_processor = TakeFirst()
    )
    # restaurant_address = scrapy.Field(
    #     # output_processor = Join(" ")
    # )
    # restaurant_tel = scrapy.Field(
    #     # output_processor = TakeFirst()
    # )
    # restaurant_url = scrapy.Field(
    #     # output_processor = TakeFirst()
    # )
    # drink_name = scrapy.Field()
    # drink_price = scrapy.Field(
    #     input_processor = MapCompose(strip_yen, strip_comma, strip_integer)
    # )
