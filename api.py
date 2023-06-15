import scrapy
class ApiSpider(scrapy.Spider):
    name = "api"
    def start_requests(self):
        yield scrapy.Request(url="http://httpbin.org/ip")
        def parse(self,response):
            print(response.text)