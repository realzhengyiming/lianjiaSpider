# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class shortInfoHome(scrapy.Item):
    homeName = scrapy.Field() # 房子的名字
    location = scrapy.Field() # 地点
    area = scrapy.Field() # 面积  单位平方米
    direction = scrapy.Field() # 朝向
    roomContent = scrapy.Field() # 房子的具体如，1室1厅1卫
    price = scrapy.Field() # 这个是物品的价格。 元/月
    homeUrl = scrapy.Field() # 详情页的url
    postDate = scrapy.Field() # 发布时间 yyyy-mm-dd


