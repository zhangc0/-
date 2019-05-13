# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from shipin.items import ShipinItem
class DianyingSpider(CrawlSpider):
    conn = Redis(host='127.0.0.1',port=6379) # 连接对象
    name = 'dianying'
    # allowed_domains = ['www.xx.com']
    start_urls = ['http://www.922dyy.com/dianying/dongzuopian/']

    rules = (
        Rule(LinkExtractor(allow=r'/dongzuopian/index\d+\.html'), callback='parse_item', follow=False), #这里需要所有页面时候改为True
    )  # 只提取页码url


    def parse_item(self, response):
        # 解析出当前页码对应页面中 电影详情页 的url
        li_list = response.xpath('/html/body/div[2]/div[2]/div[2]/ul/li')
        for li in li_list:
            # 解析详情页的url
            detail_url = 'http://www.922dyy.com' + li.xpath('./div/a/@href').extract_first()
            #
            ex = self.conn.sadd('mp4_detail_url',detail_url) # 有返回值
            # ex == 1 该url没有被请求过     ex==0在集合中,该url已经被请求过了
            if ex==1:
                print('有新数据可爬.....')
                yield scrapy.Request(url=detail_url,callback=self.parse_detail)
            else:
                print('暂无新数据可以爬取')

    def parse_detail(self,response):
        name = response.xpath('//*[@id="film_name"]/text()').extract_first()
        m_type = response.xpath('//*[@id="left_info"]/p[1]/text()').extract_first()
        print(name,'--',m_type)
        item = ShipinItem() #实例化
        item['name'] = name
        item['m_type'] = m_type

        yield item
