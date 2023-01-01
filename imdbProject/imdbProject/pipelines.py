# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient

class ImdbPipeline:

    collection_name = "IMDB"

    def open_spider(self, spider):
        self.client = MongoClient("mongodb://localhost:27017")
        db = self.client["IMDB"]
        # self.collection.drop()
        self.imdb = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.imdb.insert_one(dict(item))
        return item

# https://www.cherryservers.com/blog/how-to-install-and-start-using-mongodb-on-ubuntu-20-04