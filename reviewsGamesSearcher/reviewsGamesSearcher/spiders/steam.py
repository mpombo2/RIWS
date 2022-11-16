from scrapy import Spider
from scrapy_splash import SplashRequest

from reviewsGamesSearcher.items import Review

import re


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
            "https://store.steampowered.com/app/943370/Bravery_and_Greed/"]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 2, 'num_scrolls': 5})

    def parse(self, response):
        href = response.css(".view_all_reviews_btn > a::attr(href)").get()
        yield SplashRequest(url=href, callback=self.parse_reviews, endpoint='execute', args={'lua_source': self.script, 'wait': 2, 'num_scrolls': 10})

    def parse_reviews(self, response):

        boxReviews = response.css(
            ".apphub_Card.modalContentLink.interactable")

        for box in boxReviews:
            review = Review()

            author = box.css(
                ".apphub_CardContentAuthorName > a::text").get().strip()
            author = re.sub(r"[^a-zA-Z0-9\s]", "", author)
            review['author'] = author

            hour = box.css(".hours::text").get().strip()
            hour = re.sub(r"[^a-zA-Z0-9\s]", "", hour)
            review['hour'] = hour

            date = box.css(".date_posted::text").get().strip()
            date = re.sub(r"[^a-zA-Z0-9\s]", "", date)
            review['date'] = date

            rank = box.css(".title::text").get().strip()
            rank = re.sub(r"[^a-zA-Z0-9\s]", "", rank)
            review['rank'] = rank

            reviewText = ' '.join(
                box.css(".apphub_CardTextContent::text").getall())
            reviewText = reviewText.replace("\n", "")
            reviewText = reviewText.replace("\t", "")
            reviewText = re.sub(r"[^a-zA-Z0-9\s]", "", reviewText)
            review['review'] = reviewText.strip()

            yield review  # Will go to your pipeline
