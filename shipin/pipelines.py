# -*- coding: utf-8 -*-

class ShipinPipeline(object):
    def process_item(self, item, spider):
        conn = spider.conn
        dic = {
            'name':item['name'],
            'm_type':item['m_type']
        }

        print('here-->')
        conn.lpush('movie_data',str(dic))
        return item
