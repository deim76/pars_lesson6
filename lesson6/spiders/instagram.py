# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy import FormRequest
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from urllib.parse import urlencode

from lesson6.items import Lesson6Item


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login = 'login'
    inst_password = '*******'
    inst_login_page = 'https://www.instagram.com/accounts/login/ajax/'
    pars_user='gefestart'
    graphql_url= 'https://www.instagram.com/graphql/query/?'

    query_hash_user = 'c9100bf9110dd6361671f113dd02e7d6' #профиль
    query_hash ={'edge_followed_by' :'c76146de99bb02f6415203be841dd25a',  # подписчики
                 'edge_follow' : 'd04b0a864b4b54837c0d870b0e77e076'}  # подписки

    #

    def parse(self, response: HtmlResponse):
      # todo get token
        csrf_token = self.get_csrf_token(response.text)
      # todo Authentication
        yield FormRequest(
            self.inst_login_page,
            method='POST',
            callback=self.parse_user,
            headers={'x-csrftoken':csrf_token},
            formdata={'username':self.inst_login,'password' :self.inst_password}
            )


    def parse_user(self,response):
        jbody = json.loads(response.text)
        if jbody.get('authenticated'):
           yield response.follow(f'/{self.pars_user}',
                                 callback=self.userdata_parse,
                                 cb_kwargs={'username':self.pars_user})



    def userdata_parse(self, response, username):
        user_id=self.get_user_id(response.text, username)
        variables={'user_id':user_id,
                       'include_chaining': True,
                       "include_reel": True,
                       "include_suggested_users": False,
                  }
        url = f'{self.graphql_url}query_hash={self.query_hash_user}&{urlencode(variables)}'
        yield response.follow(url,
                              callback=self.user_parse,
                              cb_kwargs={'user_id':user_id,'type_data':'parse_user'})

    def user_parse(self,response,user_id,type_data):
        jbody = json.loads(response.text).get('data').get('user')
        item = jbody.get('reel')
        item_loader = ItemLoader(Lesson6Item(), response)
        item_loader.add_value('type_data', type_data)
        for field in Lesson6Item().fields:
            item_loader.add_value(field, item['user'].get(field))
        yield item_loader.load_item()
        variables = {'id': user_id,
                     "first": 12,
                     'fetch_mutual': False,
                     "include_reel": True
                     }
        for key, value in self.query_hash.items():
           url = f'{self.graphql_url}query_hash={value}&{urlencode(variables)}'
           yield response.follow(url,
                              callback=self.data_parse,
                              cb_kwargs={'user_id': user_id, 'type_data': key})

    def data_parse(self,response,user_id,type_data):
        jbody = json.loads(response.text).get('data').get('user')
        if jbody.get(type_data).get('page_info').get('has_next_page'):
                path={'after':jbody.get(type_data).get('page_info').get('end_cursor')}
                url = f'{response.url}&{urlencode(path)}'
                print(url)
                yield response.follow(url,
                                      callback=self.data_parse,
                                      cb_kwargs={'user_id': user_id,'type_data':type_data})
        items=jbody.get(type_data).get('edges')
        print(len(items))
        for item in items:
                print(item)
                item_loader=ItemLoader(Lesson6Item(),response)
                item_loader.add_value('parrent',user_id)
                item_loader.add_value('type_data',type_data)
                for field in Lesson6Item().fields:
                    item_loader.add_value(field,item['node'].get(field))
                yield item_loader.load_item()


    def get_user_id(self,text,username):
        result = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(result).get('id')

    def get_csrf_token(self,text):
        result = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return result.split(':').pop().replace('"', '')

