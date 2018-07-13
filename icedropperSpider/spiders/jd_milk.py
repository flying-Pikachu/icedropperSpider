# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
# from jd.items import goodsItem
from scrapy.selector import Selector
import scrapy
import json

from icedropperSpider.items import goodsItem


class jd_spider(Spider):
    name = "jd"
    start_urls = ["https://list.jd.com/list.html?cat=1320,5019,12215"]

    # from the first page, we can only get the ID, name, and link, others information we can get from the detail page
    def parse(self, response):
        sel = Selector(response)
        goods = sel.xpath('//li[@class="gl-item"]')
        for good in goods:
            item1 = goodsItem()
            item1['ID'] = good.xpath('./div/@data-sku').extract()
            item1['name'] = good.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
            item1['link'] = good.xpath('./div/div[@class="p-img"]/a/@href').extract()
            url = "http:" + item1['link'][0] + "#comments-list"
            yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_shop_name)

    # get the shop's name
    def parse_shop_name(self, response):
        item1 = response.meta['item']
        sel = Selector(response)
        item1['shop_name'] = sel.xpath('//div[@class="name"]/a/@title').extract()
        if len(item1['shop_name']) == 0:
            item1['shop_name'] = sel.xpath('//div[@class="shopName"]/strong/span/a/text()').extract()
        if len(item1['shop_name']) == 0:
            item1['shop_name'] = "自营"
        url = "http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=" + str(item1['ID'][0])
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_comment_num)

    # get the comment people's num
    def parse_comment_num(self, response):
        item1 = response.meta['item']
        js = json.loads(response.body)
        item1['comment_num'] = js['CommentsCount'][0]['CommentCount']
        num = item1['ID']
        url = "http://pm.3.cn/prices/pcpmgets?callback=jQuery&skuids=" + num[0] + "&origin=2"
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_price)

    # get the price of the merchant and return
    def parse_price(self, response):
        item1 = response.meta['item']
        temp1 = str(response.body).split('jQuery([')
        print(temp1[1])
        s = temp1[1].split(']')[0]
        print(s)
        js = json.loads(s)
        print(js)
        if 'pcp' in js:
            item1['price'] = js['pcp']
        else:
            item1['price'] = js['p']
        yield item1