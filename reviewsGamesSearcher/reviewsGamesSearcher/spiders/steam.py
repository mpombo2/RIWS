from scrapy import Spider
from scrapy_splash import SplashRequest

from datetime import datetime

from reviewsGamesSearcher.items import Review

import re
import locale


class SteamSpider(Spider):
    name = "steam"

    #Lenguages de reseñas soportado: 'es' para español y 'en' para ingles
    scrapy_language = "en"

    #Script de Lua para scrollear y acceder a la página de reviews
    script = """
function main(splash, args)
    --Deshabilitar imagenes para que carga mas rapido
    splash.images_enabled = false

    --Establecemos tiempo de espera entre scroll
    local scroll_delay = 1.0

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
    assert(splash:go{splash.args.url, headers={
        ["Accept-Language"] = splash.args.language,
    }})
    splash:wait(5.0)
    for _ = 1, splash.args.num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
  
end
"""

    def start_requests(self):
        urls = [
            "https://store.steampowered.com/app/813780/Age_of_Empires_II_Definitive_Edition/"
            #"https://store.steampowered.com/app/431960/Wallpaper_Engine/"
            ]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.script, 'timeout': 15, 'num_scrolls': 5})

    def parse(self, response):
        href = response.css(".view_all_reviews_btn > a::attr(href)").get()

        #Reseñas en español
        if (self.scrapy_language == "es"):
            yield SplashRequest(url=href, callback=self.parse_reviews_es, endpoint='execute', args={'lua_source': self.script, 'timeout': 120, 'num_scrolls': 100, 'language': 'es'})
        #Reseñas en ingles
        else:
            yield SplashRequest(url=href, callback=self.parse_reviews_en, endpoint='execute', args={'lua_source': self.script, 'timeout': 120, 'num_scrolls': 100, 'language': 'en'})        

    #Parseo de reseñas en español
    def parse_reviews_es(self, response):
        #Extraemos la review
        boxReviews = response.css(
            ".apphub_Card.modalContentLink.interactable")

        #Obtenemos cada atributo de la review
        for box in boxReviews:
            #Formateo de atributos que no dependen del idioma (author, rank y review)
            review = self.parse_reviews_common(box)

            #Formateo de horas jugadas en español (ejemplo: convertir de 1.000,5 a 1000)
            hour = box.css(".hours::text").get().strip()
            hour = re.sub(r"[^0-9.,]", "", hour)
            hour = (hour.split('.'))[0].replace(',','')
            review['hour'] = int(hour)

            #Formateo de fecha en español (ejemplo: convertir 'Publicada el 18 de noviembre de 2022 a '2022-11-18')
            date = box.css(".date_posted::text").get().strip()
            date = re.sub(r"[^a-zA-Z0-9\s]", "", date)
            review['date'] = self.format_date(date, "es")

            review['language'] = "es"

            yield review 

    #Parseo de reseñas en ingles
    def parse_reviews_en(self, response):
        #Extraemos la review
        boxReviews = response.css(
            ".apphub_Card.modalContentLink.interactable")

        #Obtenemos cada atributo de la review
        for box in boxReviews:
            #Formateo de atributos que no dependen del idioma (author, rank y review)
            review = self.parse_reviews_common(box)

            #Formateo de horas en ingles (ejemplo: convertir de 1,000.5 a 1000)
            hour = box.css(".hours::text").get().strip()
            hour = re.sub(r"[^0-9.,]", "", hour)
            hour = (hour.split(','))[0].replace('.','')
            review['hour'] = int(hour)

            #Formateo de fecha en ingles (ejemplo: convertir 'Posted 18 november 2022' a '2022-11-18')
            date = box.css(".date_posted::text").get().strip()
            date = re.sub(r"[^a-zA-Z0-9\s]", "", date)
            review['date'] = self.format_date(date, "en")

            review['language'] = "en"

            yield review 

    #Funcion que construye los atributos que no dependen del idioma (author, rank, review)
    def parse_reviews_common(self, box):
        review = Review()

        if (box.css(".apphub_CardContentAuthorName > a::text").get() != None):
            author = box.css(
                ".apphub_CardContentAuthorName > a::text").get().strip()
            author = re.sub(r"[^a-zA-Z0-9\s]", "", author)
            review['author'] = author
        else:
            review['author'] = " "

        rank = box.css(".title::text").get().strip()
        rank = re.sub(r"[^a-zA-Z]", "", rank)
        review['rank'] = (rank == "Recommended")

        reviewText = ' '.join(
            box.css(".apphub_CardTextContent::text").getall())
        reviewText = reviewText.replace("\n", "")
        reviewText = reviewText.replace("\t", "")
        reviewText = re.sub(r"[^a-zA-Z0-9\s]", "", reviewText)
        review['review'] = reviewText.strip()

        return review

    def format_date(self, date, language): 
        #Formateo de fechas en ingles
        if (language == "en"):
            date = date.replace('Posted ', '')
        #Formateo de fechas en español
        else:
            date = date.replace('Publicada el ', '').replace('de ', '')
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

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