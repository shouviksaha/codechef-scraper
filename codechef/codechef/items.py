from scrapy.item import Item, Field

class Problem(Item):
    title = Field()
    content = Field()
