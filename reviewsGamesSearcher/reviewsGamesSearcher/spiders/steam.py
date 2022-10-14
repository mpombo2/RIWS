import json
from scrapy import Spider
from scrapy_splash import SplashRequest


class SteamSpider(Spider):
    name = "steam"

    def start_requests(self):
        urls = [
            # "https://store.steampowered.com/app/787810/Rogue_Heroes_Ruins_of_Tasos/",
            # "https://steamcommunity.com/app/787810/reviews/?browsefilter=toprated&snr=1_5_100010_",
            "https://store.steampowered.com/app/1551360/Forza_Horizon_5/"]

        script = """
    function main(splash, args)
        splash:go(args.url)
        local scroll_to = splash:jsfunc("window.scrollTo")
        scroll_to(0, document.body.scrollHeight)
        return {png=splash:png()}
    end
"""

        for url in urls:
            # yield Request(url=url, callback=self.parse)
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 5},
                                )

    def parse(self, response):
        page = response.url.split("/")[2]
        filename = f'steam-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Guardado fichero {filename}')

        json.loads(response.text)
