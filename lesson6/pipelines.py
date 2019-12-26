# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from bson import DBRef

from lesson6.settings import mongo_client


class Lesson6Pipeline(object):
    def process_item(self, item, spider):
        print(item._values.get('username'))
        data_base = mongo_client[spider.name]
        collection = data_base[item._values.get('type_data')]
        pars_user_collection=data_base['parse_user']
        pars_user=pars_user_collection.find({'id':item._values.get('parrent')})
        if pars_user.count():
            item._values['parrent'] = pars_user[0]
        collection.insert(item)
        return item
