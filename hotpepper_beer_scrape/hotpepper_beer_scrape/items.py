# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
import re

# `店名` と `住所` の先頭にある `改行` と `タブ` の削除（スペースも削除できる）
def strip_spaces(element):
    return element.strip()

# ページ内にある絶対パスのURLから不要なディレクトリ名を削除
def strip_url(element):
    if element:
        return element.replace("sharestore/", "")
    return element

# 価格を不要な文字列を削除
def strip_yen(element):

    pattern = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込）$")
    pattern2 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    pattern3 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税込(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    pattern4 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込み(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    pattern5 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税込み(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    pattern6 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税抜(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    pattern7 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税抜(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    pattern8 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税抜き(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    pattern9 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税抜き(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")

    # 価格に何も入っていなかったら空とする
    if element is None:
        return ""

    # 440円（税込）
    elif pattern.match(element):
        return re.sub(pattern, r"\1", element)

    # 500円（税込550円）
    elif pattern2.match(element):
        return re.sub(pattern2, r"\3", element)

    # 600円(税込660円)
    elif pattern3.match(element):
        return re.sub(pattern3, r"\3", element)

    # 500円（税込み550円）
    elif pattern4.match(element):
        return re.sub(pattern4, r"\3", element)

    # 600円(税込み660円)
    elif pattern5.match(element):
        return re.sub(pattern5, r"\3", element)

    # 500円（税抜550円）
    elif pattern6.match(element):
        return re.sub(pattern6, r"\1", element)

    # 600円(税抜660円)
    elif pattern7.match(element):
        return re.sub(pattern7, r"\1", element)

    # 500円（税抜きみ550円）
    elif pattern8.match(element):
        return re.sub(pattern8, r"\1", element)

    # 600円(税抜きみ660円)
    elif pattern9.match(element):
        return re.sub(pattern9, r"\1", element)

    # elif "円（税込）" in element:
    #     return element.replace("円（税込）", "")

    # elif "円(税込)" in element:
    #     return element.replace("円(税込)", "")

    # elif "円（税込み）" in element:
    #     return element.replace("円（税込み）", "")

    # elif "円(税込み)" in element:
    #     return element.replace("円(税込み)", "")

    # elif "円（税抜）" in element:
    #     return element.replace("円（税抜）", "")

    # elif "円(税抜)" in element:
    #     return element.replace("円(税抜)", "")

    # elif "円（税抜き）" in element:
    #     return element.replace("円（税抜き）", "")

    # elif "円(税抜き)" in element:
    #     return element.replace("円(税抜き)", "")



    # 
    # elif r"^(\d+)円（税込）" in element:
    #     return re.sub(r"^(\d+)円（税込）", "", element)

    # 500円（税込550円） → 550
    # elif r"(\d+)円（税込(\d+)円）" in element:
    #     return re.sub(r"(\d+)円（税込(\d+)円）", "", element)

    # # 500円(税込550円) → 550
    # elif r"(\d+)円\(税込(\d+)円\)" in element:
    #     return re.sub(r"(\d+)円\(税込(\d+)円\)", r"\2", element)

    # elif "円" in element:
    #     return element.replace("円", "")

    # elif "円" in element:
    #     return element.replace("円", "")

    else:
        return element

# 価格からカンマを削除
def strip_comma(element):
    if element:
        return element.replace(",", "")
    return element

# 価格を数値型に変換
def convert_integer(element):
    if element:
        return int(element)
    return 0


class RestaurantItem(scrapy.Item):
    restaurant_name = scrapy.Field(
        input_processor = MapCompose(strip_spaces),
        output_processor = TakeFirst()
    )

    restaurant_address = scrapy.Field(
        input_processor = MapCompose(strip_spaces),
        output_processor = TakeFirst()
    )

    restaurant_tel = scrapy.Field(
        output_processor = TakeFirst()
    )

    restaurant_url = scrapy.Field(
        input_processor = MapCompose(strip_url),
        output_processor = TakeFirst()
    )

    drink_name = scrapy.Field()

    drink_price = scrapy.Field(
        input_processor = MapCompose(strip_yen, strip_comma)
    )
