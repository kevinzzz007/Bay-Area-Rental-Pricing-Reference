__author__ = 'RunzeZhao'
from scrapy import Spider
from scrapy.selector import Selector
from rental_pricing_project.items import RentalPricingProjectItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy
import time

class RentalPricingSpider(Spider):
    name = 'rental_pricing'
    allowed_domains=['sfbay.craigslist.org']
    start_urls=[
        'https://sfbay.craigslist.org/search/apa',
    ]
    rules = (
        Rule(LinkExtractor(allow=r'search/'),
             callback='parse', follow=True),
            )

    def parse(self, response):
        time.sleep(10)
        text_for_one_listing = Selector(response).xpath('//div[@class="rightpane"]/div[3]/p')
        for link in text_for_one_listing:
            item= RentalPricingProjectItem()
            item['link']= link.xpath('span/span[2]/a/@href').extract()[0]
            item['price']=link.xpath('span/span[3]/span[1]/text()').extract()[0]
            item['size'] =link.xpath('span/span[3]/span[2]/text()').extract()[0]
            request = scrapy.Request('https://sfbay.craigslist.org' + link.xpath('span/span[2]/a/@href').extract()[0],
                                     meta={'my_meta_item':item},callback=self.parse_one_listing_for_location)
            yield request
        for url in response.xpath('//*[@id="searchform"]/div[2]/div[2]/div/span/span[2]/a[3]/@href').extract():
            url = 'https://sfbay.craigslist.org' + url
            yield scrapy.Request(url, callback=self.parse)

    def parse_one_listing_for_location(self, response):
        google_map_links = Selector(response).xpath('//section[@class="body"]/section[2]/div[1]/div[1]/p/small')
        item= response.meta['my_meta_item']
        try:
            item['google_map_link'] = google_map_links.xpath('a[1]/@href').extract()[0]
        except IndexError:
            item['google_map_link'] = 'no_google_map_link'
        yield item