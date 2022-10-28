# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Review(scrapy.Item):
    author = scrapy.Field()
    hour = scrapy.Field()
    date = scrapy.Field()
    rank = scrapy.Field()
    review = scrapy.Field()
