# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem
from scrapy import Request
from urllib.parse import quote

class JdshopSpider(scrapy.Spider):
    name = 'jdshop'
    allowed_domains = ['list.jd.com']
    base_urls = 'https://list.jd.com/list.html?cat=670,671,672'

    def start_requests(self):

        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = self.base_urls
            yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        results = response.css('#plist ul.gl-warp li.gl-item')
        for result in results:
            item = JdItem()

            item['title'] = result.css('div.p-name em::text').extract_first()
            item['price'] = result.css('div.p-price i::text').extract_first()
            item['commit'] = result.css('div.p-name i::text').extract_first()
            item['img'] = result.css('div.p-img img::attr(src)').extract_first()
            item['shop'] = result.css('div.p-shop a::attr(title)').extract_first()
            yield item