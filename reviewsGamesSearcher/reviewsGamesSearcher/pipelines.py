# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class ReviewsgamessearcherPipeline:
    listItems = []
   

    def process_item(self, item, spider):
        self.listItems.append(item)
        return item

    def close_spider(self, spider):

        doc = {
            'author': 'author_name',
            'text': 'Interensting content...',
            'timestamp': datetime.now(),
        }
        es = Elasticsearch('https://localhost:9200',
                       verify_certs=False,  basic_auth=('elastic', 'es1234'),)

        actions = []
        for item in self.listItems:
            action = {
                "_index": "steam",
                "_source": dict(item)
                }
            actions.append(action)

        helpers.bulk(es, actions)

        print("spider closed")
        #print(self.listItems)
