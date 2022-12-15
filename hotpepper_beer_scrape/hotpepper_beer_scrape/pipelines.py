# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

# class CheckItemPipeline:
#     def process_item(self, item, spider):
#         item['restaurant_name'] = item['restaurant_name'].replace("\n\t\t\t\t\t\t", "")
#         return item

# 値のバリデーションチェック
class ValidationPipeline(object):
    def process_item(self, item, spider):
        if item['restaurant_address'] is None or item['restaurant_address'] == '':
            raise DropItem('Missing value: restaurant_address')

        if item['drink_name'] is None or item['drink_name'] == '':
            raise DropItem('Missing value: drink_name')

        if item['drink_price'] is None or item['drink_price'] == '':
            raise DropItem('Missing value: drink_price')

        return item
