# -*- coding: utf-8 -*-
# Author : Jay
# writeTime : 2019/11/18 intern ing!

from scrapy_redis.spiders import RedisSpider
from Jay_Redis_slave.InsertIntoDatabase import no_dup_request
from scrapy.selector import Selector
from Jay_Redis_slave.items import MovieItem
defaultEncoding = 'utf-8'


class MySpider(RedisSpider):
    name = 'SlaveDouban'
    allowed_domains = ['movie.douban.com']
    redis_key = 'content_urls'
    print('>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>豆瓣slave端爬虫启动')

    # TODO 对抓取到的播放url需要进行处理，此处的url不是直连的url，而是带有自身广告的各种接口的url，无法直接破解播放
    def parse(self, response):
        try:
            verify = no_dup_request(response.url)
            if verify:
                movieItem = MovieItem()
                selector = Selector(response)
                movieItem['url'] = response.url
                movieItem['title'] = '|'.join(selector.xpath(r'//div[@id="content"]/h1/span[1]/text()')
                                              .extract()).strip()
                movieItem['director'] = '|'.join(selector.xpath(r'//div[@id="info"]/span[1]/span[2]/a/text()')
                                                 .extract()).strip()
                movieItem['screenwriter'] = '|'.join(selector.xpath(r'//div[@id="info"]/span[2]/span[2]/a/text()')
                                                     .extract()).strip()
                movieItem['actors'] = '|'.join(selector.xpath(r'//div[@id="info"]/span[@class="actor"]/span[2]/a/text()')
                                               .extract())
                movieItem['category'] = '|'.join(selector.xpath(r'//div[@id="info"]/span[@property="v:genre"]/text()')
                                                 .extract()).strip()
                movieItem['country'] = selector.xpath(r'//div[@id="info"]/span[./text()="制片国家/地区:"]/following::'
                                                      r'text()[1]').extract_first().strip()
                movieItem['langrage'] = selector.xpath(r'//div[@id="info"]/span[./text()="语言:"]/following::text()['
                                                       r'1]').extract_first().strip()
                movieItem['initial'] = selector.xpath('//span[@property="v:initialReleaseDate"]/text()') \
                    .extract_first().strip()
                movieItem['runtime'] = selector.xpath(r'//div[@id="info"]/span[@property="v:runtime"]/text()')\
                    .extract_first()
                playableUrl = '|'.join(selector.xpath(r'//div[@class="gray_ad"]/ul/li/a/@href')
                                       .extract()).strip()
                if playableUrl:
                    movieItem['playUrl'] = playableUrl
                else:
                    movieItem['playUrl'] = '/'
                movieItem['rate'] = selector.xpath(r'//div[@class="rating_self clearfix"]/strong/text()')\
                    .extract_first()
                movieItem['starPeople'] = selector.xpath(r'//a[@class="rating_people"]/span/text()')\
                    .extract_first()
                movieItem['preShowUrl'] = selector.xpath(r'//div[@id="related-pic"]/ul[1]/li[1]/a/@href')\
                    .extract_first()
                movieItem['intro'] = '|'.join(selector.xpath(r'//span[@property="v:summary"]/text()').extract()).strip()
                movieItem['icon'] = selector.xpath(r'//div[@id="mainpic"]/a/img/@src').extract_first().strip()
                yield movieItem
        except Exception as e:
            print('extract error %s, %s' % (e, response.url))



