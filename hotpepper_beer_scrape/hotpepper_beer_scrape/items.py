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

    listed_price_type1 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    listed_price_type2 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税込(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    listed_price_type3 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込み(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    listed_price_type4 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税込み(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    listed_price_type5 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税抜(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    listed_price_type6 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税抜(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    listed_price_type7 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税抜き(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円）$")
    listed_price_type8 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税抜き(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\)$")
    listed_price_type9 = re.compile(r"^各(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円（税込）$")
    listed_price_type10 = re.compile(r"^各(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\(税抜\)$")
    listed_price_type11 = re.compile(r"^各(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円$")
    listed_price_type12 = re.compile(r"^\\(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)$")
    listed_price_type13 = re.compile(r"^(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円\((0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)円税込\)$")

    # 価格に何も入っていなかったら空とする
    if element is None:
        return ""

    # 500円（税込550円）
    elif listed_price_type1.match(element):
        return re.sub(listed_price_type1, r"\3", element)

    # 600円(税込550円)
    elif listed_price_type2.match(element):
        return re.sub(listed_price_type2, r"\3", element)

    # 500円（税込み550円）
    elif listed_price_type3.match(element):
        return re.sub(listed_price_type3, r"\3", element)

    # 600円(税込み550円)
    elif listed_price_type4.match(element):
        return re.sub(listed_price_type4, r"\3", element)

    # 550円（税抜500円）
    elif listed_price_type5.match(element):
        return re.sub(listed_price_type5, r"\1", element)

    # 550円(税抜500円)
    elif listed_price_type6.match(element):
        return re.sub(listed_price_type6, r"\1", element)

    # 550円（税抜き500円）
    elif listed_price_type7.match(element):
        return re.sub(listed_price_type7, r"\1", element)

    # 550円(税抜き500円)
    elif listed_price_type8.match(element):
        return re.sub(listed_price_type8, r"\1", element)

    # 各550円（税込）
    elif listed_price_type9.match(element):
        return re.sub(listed_price_type9, r"\1", element)

    # 各500円(税抜)
    elif listed_price_type10.match(element):
        return re.sub(listed_price_type10, r"\1", element)

    # 各550円
    elif listed_price_type11.match(element):
        return re.sub(listed_price_type11, r"\1", element)

    # \550
    elif listed_price_type12.match(element):
        return re.sub(listed_price_type12, r"\1", element)

    # 500円(550円税込)
    elif listed_price_type13.match(element):
        return re.sub(listed_price_type13, r"\3", element)

    elif "円（税込）" in element:
        return element.replace("円（税込）", "")

    elif "円(税込)" in element:
        return element.replace("円(税込)", "")

    elif "円（税込み）" in element:
        return element.replace("円（税込み）", "")

    elif "円(税込み)" in element:
        return element.replace("円(税込み)", "")

    elif "円（税抜）" in element:
        return element.replace("円（税抜）", "")

    elif "円(税抜)" in element:
        return element.replace("円(税抜)", "")

    elif "円(税抜）" in element:
        return element.replace("円(税抜）", "")

    elif "円（税抜き）" in element:
        return element.replace("円（税抜き）", "")

    elif "円(税抜き)" in element:
        return element.replace("円(税抜き)", "")

    elif "円（税別）" in element:
        return element.replace("円（税別）", "")

    elif "円(税別)" in element:
        return element.replace("円(税別)", "")

    elif "円～" in element:
        return element.replace("円～", "")

    elif "円" in element:
        return element.replace("円", "")

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

    restaurant_genre = scrapy.Field(
        input_processor = MapCompose(strip_spaces),
        # output_processor = TakeFirst()
    )

    drink_name = scrapy.Field()

    drink_price = scrapy.Field(
        input_processor = MapCompose(strip_yen, strip_comma)
    )
