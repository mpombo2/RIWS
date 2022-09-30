from scrapy import Spider, Request

class SteamSpider(Spider):
    name = "steam"

    def start_requests(self):
        urls = [""]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page = response.url
        print(page)