# -*- coding: utf-8 -*-
from pymongo import MongoClient
from scrapy import logformatter
import traceback
from scrapy.exceptions import DropItem

class MongodbPipeline(object):
    MONGODB_SERVER = '122.51.95.201'
    MONGODB_PORT = 27017
    MONGODB_DB = 'JayMongo'
    MONGODB_USER = 'root'
    MONGODB_PWD = '919169807'

    def __init__(self):
        try:
            self.client = MongoClient(host=self.MONGODB_SERVER, port=self.MONGODB_PORT)
            self.db = self.client[self.MONGODB_DB]
            self.db.authenticate(name=self.MONGODB_USER, password=self.MONGODB_PWD)
            self.col = self.db["movie_content"]
        except Exception:
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SingleMONGODB_SERVER', '122.51.95.201')
        cls.MONGODB_PORT = crawler.settings.getint('SingleMONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SingleMONGODB_DB', 'JayMongo')
        cls.MONGODB_USER = crawler.settings.get('SingleMONGODB_USER', 'root')
        cls.MONGODB_PWD = crawler.settings.get('SingleMONGODB_PWD', '919169807')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        # if item['a'] == 0:
        #     raise DropItem("Duplicate item found: %s" % item)
        movie_detail = {
            'url': item.get('url'),
            'title': item.get('title'),
            'director': item.get('director'),
            'screenwriter': item.get('screenwriter'),
            'actors': item.get('actors'),
            'category': item.get('category'),
            'country': item.get('country'),
            'langrage': item.get('langrage'),
            'initial': item.get('initial'),
            'runtime': item.get('runtime'),
            'playUrl': item.get('playUrl'),
            'rate': item.get('rate'),
            'starPeople': item.get('starPeople'),
            'preShowUrl': item.get('preShowUrl'),
            'intro': item.get('intro'),
            'icon': item.get('icon')
        }
        result = self.col.insert(movie_detail)
        print('[success] insert ' + item['url'] + ' title:' + item['title'])
        return item

