from pathlib import Path
import scrapy

class QuotesSpider(scrapy.Spider):
    
    name = "quotes"

    # You can define start_urls as a list of URLs to start crawling from
    # start_urls = [
    #     "https://quotes.toscrape.com/page/1/",
    #     "https://quotes.toscrape.com/page/2/",
    # ]

    # Alternatively, you can define a start method to yield requests
    async def start(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    # parse is scrapy's default callback method
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                # "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            # # use urljoin to make absolute URL
            # next_page = response.urljoin(next_page)
            # # yields a new request to the next page, registering itself as callback to handle the data extraction for the next page and to keep the crawling going through all the pages.
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, self.parse)