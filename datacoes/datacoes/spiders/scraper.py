import scrapy
import datetime

class DataCoesSpider(scrapy.Spider):
    name = 'scrap_coes'
    start_urls = [
        "https://www.coes.org.pe/Portal/home/"
    ]
    custom_settings = {
        'FEED_URI': 'data.json',
        'FEED_FORMAT': 'json',
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'user_me',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        events = response.xpath('//div[@class="col-md-6 col-sm-6-2"][1]//h2/a/text()').getall()
        events_out = dict()
        for i,event in enumerate(events):
            date = response.xpath(f'//div[@class="col-md-6 col-sm-6-2"][1]//div[@class="coes-preview-list"]/div[{i+1}]/p/text()').get()
            date = [datetime.datetime.now().year,date]
            description = response.xpath(f'//div[@class="col-md-6 col-sm-6-2"][1]//div[@class="coes-preview-list"]/div[{i+1}]/div/p/text()').get()
            events_out[event] = {'description':description,'date':date}       
        
        yield {
        'events':events_out
        }
    


        
        
        