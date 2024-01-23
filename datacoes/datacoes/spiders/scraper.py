import scrapy
import datetime

class DataCoesSpider(scrapy.Spider):
    name = 'scrap_events'
    start_urls = [
        "https://www.coes.org.pe/Portal/home/"
    ]
    custom_settings = {
        'FEED_URI': 'data_events.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 5,
        'MEMUSAGE_LIMIT_MB': 1024,
        'MEMUSAGE_NOTIFY_MAIL': ["user@mail.com"],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'user_me',
        'FEED_EXPORT_ENCODING': "utf-8"
    }

    def parse(self, response):
        rel_24h_events = response.xpath('//div[@class="col-md-6 col-sm-6-2"][1]//h2/a/text()').getall()
        max_dem_events = response.xpath('//div[@class="col-md-6 col-sm-6-2"][2]//h2/a/text()').getall()
        events_out = dict()
        event_max_out = dict()
        for i,event in enumerate(rel_24h_events):
            date = response.xpath(f'//div[@class="col-md-6 col-sm-6-2"][1]//div[@class="coes-preview-list"]/div[{i+1}]/p/text()').get()
            description = response.xpath(f'//div[@class="col-md-6 col-sm-6-2"][1]//div[@class="coes-preview-list"]/div[{i+1}]/div/p/text()').get()
            events_out[event] = {'description':description.replace("\r\n",""),'date':date}       
                
        for i,event in enumerate(max_dem_events):
            description = response.xpath(f'//div[@class="col-md-6 col-sm-6-2"][2]//div[@class="coes-preview-list"]/div[{i+1}]/div/p/text()').get()
            event_max_out[event.replace("MÁXIMA DEMANDA","")] = {'description':description.replace("\r\n","")} 

        yield {
        'rel_24h_events':events_out,
        'max_dem_events':event_max_out
        }
        
        
        