from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson6 import settings
from lesson6.spiders.instagram import InstagramSpider

if __name__=='__main__':
    cr_settings=Settings()
    cr_settings.setmodule(settings)
    process=CrawlerProcess(settings=cr_settings)
    process.crawl(InstagramSpider)
    process.start()