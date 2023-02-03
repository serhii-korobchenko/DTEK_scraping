import scrapy


class DtekAlarmSwitchOffSpider(scrapy.Spider):
    name = 'dtek_alarm_switch_off'
    allowed_domains = ['dtek-kem.com.ua']
    start_urls = ['http://dtek-kem.com.ua/']

    def parse(self, response):
        pass
