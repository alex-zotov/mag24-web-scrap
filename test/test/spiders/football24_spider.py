from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "football24"
    # custom_settings = {
    #        'MONGO_COLLECTION_NAME': name
    #     }

    async def start(self):
        urls = [
            "https://football24.ru/articles/page/1/",
            "https://football24.ru/articles/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        
        # на сайте идёт перенаравление 
        # /articles/page/1/ => /articles/
        # чтоб было удобно сохраним стартовую станичку под номером 1
        if page=='articles':
            page='1'
        
        # сохраняем в файл
        filename = f"./data/articles-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        # парсим страничку
        for article in response.xpath('//*[@id="dle-content"]/article'):
            yield {
                'url': article.xpath('.//*[@itemprop="headline"]//a/@href').get(),
                'title': ' '.join(article.xpath('.//*[@itemprop="headline"]//a/text()').getall()),
                'date_published': article.xpath('.//time[@itemprop="datePublished"]/@datetime').get(),
                'description': ' '.join(article.xpath('.//*[@itemprop="description"]/text()').getall())
            }