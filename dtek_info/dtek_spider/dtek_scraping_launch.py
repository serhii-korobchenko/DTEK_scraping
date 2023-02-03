import scrapy
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from selenium import webdriver
import time
from scrapy.selector import Selector



class DtekAlarmSwitchOffSpider(scrapy.Spider):
    name = 'dtek_alarm_switch_off'

    # start custom settings
    custom_settings = {

        # 'ITEM_PIPELINES': {
        # 'alarm_spyder.pipelines.NewsSpyderPipeline': 400
        #                    },

        "FEEDS": {
            'dtek_info.json': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'overwrite': True,

            },
        }

        # "SPIDER_MIDDLEWARES": {
        #     'alarm_spyder.middlewares.NewsSpyderMiddleware': 548,
        # }
    }
    # stop custom settings


    allowed_domains = ['dtek-kem.com.ua']
    start_urls = ['https://www.dtek-kem.com.ua/ua/shutdowns']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    def parse(self, response):

        self.driver.get(response.url)
        time.sleep(5)

        # Enter street
        street = self.driver.find_element(By.ID, 'street')
        street.clear()
        street.send_keys("Зодч")
        time.sleep(2)
        street.send_keys(Keys.RETURN)
        time.sleep(2)


        # Enter Building
        bld = self.driver.find_element(By.ID, 'house_num')
        bld.clear()
        bld.send_keys("62/А")
        time.sleep(2)
        bld.send_keys(Keys.RETURN)
        time.sleep(2)






        scrapy_selector = Selector(text=self.driver.page_source)
        table = scrapy_selector.xpath('//*[@class="tableRenderElem"]//tbody').extract()
        # rows = table.xpath('/tr')
        #row = rows[1]
        # result = row.xpath('td//text()')[1].extract()
        print(f'ROWS----------------------> {table}')



        # for _ in range(1, 24):
        # yield {
        #     "result": rows.extract()
        #         }




        self.driver.close()


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(DtekAlarmSwitchOffSpider)
    # yield runner.crawl(AirRaidAlarmsKyivSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished