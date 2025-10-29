# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class MongoPipeline:
    # azot
    # попробовал название коллекции инициализировать в пауке
    # collection_name = "scrapy_items"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            # azot:
            # если в настройках не указано, то по умолчанию создаст базу items
            # mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
            # в settings.py явно указал имя базы
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        # collection_name = spider.settings.get('MONGO_COLLECTION_NAME')
        collection_name = spider.name
        
        # проверяем, существует ли уже запись с таким url
        unique_field = 'url'

        if self.db[collection_name].find_one({unique_field: item[unique_field]}):
            spider.logger.info(f'Duplicate item found: {item[unique_field]}')
            raise DropItem(f"Duplicate item found: {item[unique_field]}")
        else:
            self.db[collection_name].insert_one(ItemAdapter(item).asdict())

        return item