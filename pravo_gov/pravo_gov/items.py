# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DocumentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    signature = scrapy.Field()
    publications = scrapy.Field()
    keywords = scrapy.Field()
    branches = scrapy.Field()
    def __setitem__(self, key, value):
        if key == 'keywords' and isinstance(value, str):
            value = value.split(', ')
        super().__setitem__(key, value)


