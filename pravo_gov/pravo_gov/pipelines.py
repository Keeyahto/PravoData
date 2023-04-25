# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from scrapy.utils.project import get_project_settings
import os

class JsonWriterPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        output_dir = settings['FEED_URI']
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        self.file = open(output_dir, 'w', encoding='cp1251')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

class PravoGovPipeline:
    def process_item(self, item, spider):
        return item
