# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class Lesson6Item(scrapy.Item):
      # define the fields for your item here like:
        _id = scrapy.Field()
        id = scrapy.Field(output_processor=TakeFirst())
        username = scrapy.Field(output_processor=TakeFirst())
        full_name = scrapy.Field(output_processor=TakeFirst())
        profile_pic_url = scrapy.Field(output_processor=TakeFirst())
        parrent = scrapy.Field(output_processor=TakeFirst())
        type_data=scrapy.Field(output_processor=TakeFirst())

