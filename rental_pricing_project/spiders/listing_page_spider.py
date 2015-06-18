__author__ = 'RunzeZhao'
from scrapy import Spider
from scrapy.selector import Selector
from rental_pricing_project.items import RentalPricingProjectItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy

class ListingPageSpider(Spider):
    name = 'listing_page'
    allowed_domains=['sfbay.craigslist.org']
    start_urls=[
        'https://sfbay.craigslist.org/search/apa',
    ]
    rules = (
        Rule(LinkExtractor(allow=r'apa\/d+'),
             callback='parse', follow=True),
            )

    def parse(self, response):
        google_map_links = Selector(response).xpath('//section[@class="body"]/section[2]/div[1]/div[1]/p/small')
        item= RentalPricingProjectItem()
        item['google_map_link'] = google_map_links.xpath('a[1]/@href').extract()[0]
        yield item

        for url in response.xpath('//*[@id="searchform"]/div[2]/div[2]/div/span/span[2]/a[3]/@href').extract():
            url = 'https://sfbay.craigslist.org' + url
            yield scrapy.Request(url, callback=self.parse)