# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QuotestoscrapePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        # Open the file in write mode when the spider is opened
        self.file = open('output.txt', 'w')

    def close_spider(self, spider):
        # Close the file when the spider is closed
        self.file.close()

    def process_item(self, item, spider):
        # Convert the item to a string and write it to the file
        line = f"Quote: {item.get('quote')}\n" \
               f"Author: {item.get('author')}\n" \
               f"Author About Link: {item.get('author_about_link')}\n" \
               f"Tags: {', '.join(item.get('tags', []))}\n" \
               f"Author Born Date: {item.get('author_born_date')}\n" \
               f"Author Born Location: {item.get('author_born_location')}\n" \
               f"\n"  # Add an empty line between items
        self.file.write(line)
