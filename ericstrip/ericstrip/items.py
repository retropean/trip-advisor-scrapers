import scrapy
from scrapy.item import Item, Field

class EricstripItem(scrapy.Item):
    url = Field()
    pass
