# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WanfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    #引用在期刊里没有数据，没法爬
    c_title = scrapy.Field()#中文标题
    e_title = scrapy.Field()#英文标题

    url = scrapy.Field()#链接

    c_author = scrapy.Field()#作者姓名 中文
    #e_author = scrapy.Field()#作者姓名 英文

    c_periodical = scrapy.Field()#期刊名称 中文
    e_periodical = scrapy.Field()  # 期刊名称 英文

    indexID = scrapy.Field() #年，卷（期）

    c_abstract = scrapy.Field()#摘要 中文
    #E_abstract = scrapy.Field()#摘要 英文

    c_keywords = scrapy.Field()#关键字 中文
   # E_keywords = scrapy.Field()#关键字 英文

    time = scrapy.Field()#出版日期
    fund = scrapy.Field()#基金项目
    units = scrapy.Field()#作者单位
    pass
