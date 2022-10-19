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
    splash.images_enabled = false
    local num_scrolls = 10
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    local drop_button = splash:select_all(".view_all_reviews_btn")[0]
    local children = drop_button:GetChildren()
    for i = 1, #children do
        print(i, children[i].Name)
    end
    
    splash:wait(splash.args.wait)
    return {
    html = splash:html(),
    png = splash:png(),
  }
end
"""
        for url in urls:
            # yield Request(url=url, callback=self.parse)
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': script, 'wait': 2})

    def parse(self, response):
        page = response.url.split("/")[2]
        filename = f'steam-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Guardado fichero {filename}')

        json.loads(response.text)
