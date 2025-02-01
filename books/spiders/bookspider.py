import scrapy

from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for product in response.css("article.product_pod"):
            item = BooksItem()
            try:
                item["title"] = product.css("h3 > a::attr(title)").get()
                item["price"] = product.css(".price_color::text").get().replace('£', '')
                item["url"] = product.css("h3 > a::attr(href)").get()
                yield item
                
            except:
                item["title"] = product.css("h3 > a::attr(title)").get()
                item["price"] = "Sold out"
                item["url"] = product.css("h3 > a::attr(href)").get()

        next_page = response.css('li.next > a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)