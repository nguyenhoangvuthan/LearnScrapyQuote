import scrapy

from quotestoscrape.items import QuotestoscrapeItem


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            author_url = quote.xpath('.//small[@class="author"]/following-sibling::a/@href').get()
            yield response.follow(author_url, self.parse_author, meta={'quote': quote})

        # Follow pagination link
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        quote_items: QuotestoscrapeItem = QuotestoscrapeItem()

        quote = response.meta['quote']
        quote_items["quote"] = quote.xpath('.//span[@class="text"]/text()').get()
        quote_items["author"] = quote.xpath('.//small[@class="author"]/text()').get()
        absolute_link: str = "https://quotes.toscrape.com"
        quote_items["quote"] = f"{absolute_link}/{quote.xpath('./span/a/@href').get()}"
        quote_items["author_born_date"] = response.xpath('//span[@class="author-born-date"]/text()').get()
        quote_items["author_born_location"] = response.xpath('//span[@class="author-born-location"]/text()').get()
        quote_items["author_description"] = response.xpath('//div[@class="author-description"]/text()').get()
        quote_items["tags"] = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()
        yield quote_items