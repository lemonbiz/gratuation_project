# -*- coding: utf-8 -*-
# Author : Jay
# writeTime : 2019/11/16 intern ing!

from scrapy_redis.spiders import RedisSpider
from Jay_Redis.utils.InsertIntoDatabase import insert_content_urls, insert_new_start_urls, insert_into_start_urls
import json
import re


class MySpider(RedisSpider):
    name = 'MasterDouban'
    allowed_domains = ['movie.douban.com']
    redis_key = 'start_urls'
    insert_into_start_urls()
    print('>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>豆瓣master端爬虫启动')
    # if filter in master_end, slave_ends read urls then delete, error pops

    def parse(self, response):
        # self.count += 1
        if re.match(r'https://movie.douban.com/j/new_', response.url):
            content = json.loads(response.text)['data']
            for info in content:
                content_url = info['url']
                if content_url:
                    insert_content_urls(content_url)

            if len(content) is 20:
                next_url = re.findall(r'start=(\d+)', response.url)[0]
                next_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1' \
                           '&start={}'.format(int(next_url)+20)
                print('>>>>>>>>>>>>>>>插入新的电影页成功<<<<<<<<<<<<<<<')
                insert_new_start_urls(next_url)
            else:
                print('>>>>>>>>>>>>>>>此类电影已爬取完毕<<<<<<<<<<<<<<<')
        else:
            content = json.loads(response.text)['subjects']
            for info in content:
                content_url = info['url']
                if content_url:
                    insert_content_urls(content_url)

            if len(content) is 100:
                # method of next page
                # length not enough = not enough for next page
                next_url = re.findall(r'(.*?)page_start=(\d+)', response.url)[0]
                next_url = next_url[0] + 'page_start={}'.format(int(next_url[1])+100)
                print('>>>>>>>>>>>>>>>插入新的电影页成功<<<<<<<<<<<<<<<')
                insert_new_start_urls(next_url)
            else:
                print('>>>>>>>>>>>>>>>此类电影已爬取完毕<<<<<<<<<<<<<<<')
        # if self.count > 10:
        #     self.crawler.engine.close_spider('queue is empty, the spider close')
