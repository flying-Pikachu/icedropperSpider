# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

#
class goodsItem(scrapy.Item):
    link = Field()          # merchant link
    ID = Field()            # merchant ID
    name = Field()          # merchant name
    comment_num = Field()   # the number of the comment people
    shop_name = Field()     # the name of the shop
    price = Field()         # the price of the merchant