# -*- coding: utf-8 -*-

import scrapy

class ShipinItem(scrapy.Item):

    name = scrapy.Field()
    m_type = scrapy.Field()

