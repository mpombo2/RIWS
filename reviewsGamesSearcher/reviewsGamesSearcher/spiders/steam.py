import json
from scrapy import Spider
from scrapy_splash import SplashRequest


class SteamSpider(Spider):
    name = "steam"

    script = """
function main(splash, args)
    splash.images_enabled = false
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, splash.args.num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
  
end
"""

    def start_requests(self):
        urls = [
            # "https://store.steampowered.com/app/787810/Rogue_Heroes_Ruins_of_Tasos/",
            # "https://steamcommunity.com/app/787810/reviews/?browsefilter=toprated&snr=1_5_100010_",
            "https://store.steampowered.com/app/1551360/Forza_Horizon_5/"]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 2, 'num_scrolls': 5})

    def parse(self, response):
        href = response.css(".view_all_reviews_btn > a::attr(href)").get()
        yield SplashRequest(url=href, callback=self.parse_reviews, endpoint='execute', args={'lua_source': self.script, 'wait': 2, 'num_scrolls': 20})

    def parse_reviews(self, response):
        authors = response.css(
            ".apphub_CardContentAuthorName > a::text").getall()
        for author in authors:
            print(author)

        hours = response.css(".hours::text").getall()
        for hour in hours:
            print(hour)

        dates = response.css(".date_posted::text").getall()
        for date in dates:
            print(date)

        ranking = response.css(".title::text").getall()
        for rank in ranking:
            print(rank)

        reviews = response.css(".apphub_CardTextContent::text").getall()
        for review in reviews:
            print(review)
