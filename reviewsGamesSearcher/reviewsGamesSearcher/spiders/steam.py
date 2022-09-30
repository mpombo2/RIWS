from scrapy import Spider, Request


class SteamSpider(Spider):
    name = "steam"

    def start_requests(self):
        urls = [
            "https://store.steampowered.com/app/787810/Rogue_Heroes_Ruins_of_Tasos/"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[2]
        filename = f'steam-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Guardado fichero {filename}')
