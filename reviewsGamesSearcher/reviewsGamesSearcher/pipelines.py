# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch, helpers
import json

class ReviewsgamessearcherPipeline:
    listItems = []

    def process_item(self, item, spider):
        self.listItems.append(json.dumps(dict(item)))
        return item

    def close_spider(self, spider):

        es = Elasticsearch('https://localhost:9200',
                           verify_certs=False,  basic_auth=('elastic', 'es1234'),)

        actions = [
            {
                "_index": "steam",
                "_source": node
            }
            for node in self.listItems
        ]
        print(actions)

        helpers.bulk(es, actions)
