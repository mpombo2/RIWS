from scrapy import Spider
from scrapy_splash import SplashRequest

from datetime import datetime

from reviewsGamesSearcher.items import Review

import re


class SteamSpider(Spider):
    name = "steam"

    script = """
function main(splash, args)
    splash.images_enabled = false
    local scroll_delay = 2.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
    assert(splash:go(splash.args.url))
    splash:wait(2.0)
    for _ = 1, splash.args.num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
  
end
"""

    def start_requests(self):
        urls = [
            "https://store.steampowered.com/app/813780/Age_of_Empires_II_Definitive_Edition/"]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.script, 'wait': 10, 'num_scrolls': 5})

    def parse(self, response):
        href = response.css(".view_all_reviews_btn > a::attr(href)").get()
        yield SplashRequest(url=href, callback=self.parse_reviews, endpoint='execute', args={'lua_source': self.script, 'wait': 30, 'num_scrolls': 10})

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
            hour = re.sub(r"[^0-9.,]", "", hour)
            review['hour'] = float(hour.replace(',',''))


            date = box.css(".date_posted::text").get().strip()
            date = re.sub(r"[^a-zA-Z0-9\s]", "", date)
            review['date'] = self.format_date(date)

            rank = box.css(".title::text").get().strip()
            rank = re.sub(r"[^a-zA-Z]", "", rank)
            review['rank'] = (rank == "Recommended")

            reviewText = ' '.join(
                box.css(".apphub_CardTextContent::text").getall())
            reviewText = reviewText.replace("\n", "")
            reviewText = reviewText.replace("\t", "")
            reviewText = re.sub(r"[^a-zA-Z0-9\s]", "", reviewText)
            review['review'] = reviewText.strip()

            yield review  # Will go to your pipeline

    def format_date(self, date): 
        date = date.replace('Posted ', '')
        if len(date.split()) < 3:
            date = date + " " + datetime.now().strftime("%Y")

        date_formated = ""
        try:
            format = "%d %B %Y"
            date_formated = datetime.strptime(date, format)
            return date_formated.strftime("%Y-%m-%d")
        except ValueError:
            format = "%B %d %Y"
            date_formated = datetime.strptime(date, format)
            return date_formated.strftime("%Y-%m-%d")