import scrapy
import json
from urllib.parse import urlencode, parse_qs, urlparse
from .utils.startlinkcreator import StartLinkCreator
from pathlib import Path
import re
from ..items import DocumentItem


class PravoGovSpiderSpider(scrapy.Spider):
    name = "pravo_gov_spider"
    allowed_domains = ["pravo.gov.ru"]
    start_urls = ["http://pravo.gov.ru/proxy/ips/"]
    doc_per_page = 200


    def start_requests(self):
        with open(Path(__file__).parent.parent / 'params.json') as f:
            params = json.load(f)
        slc = StartLinkCreator(**params)
        start_link = slc.get_start_link()
        yield scrapy.Request(start_link, self.parse)


    def parse(self, response):
        # Получаем количество документов на странице и общее число документов
        doc_n = int(response.css('.large::text').get())
        # Вычисляем количество страниц
        num_pages = doc_n // self.doc_per_page + (1 if doc_n % self.doc_per_page > 0 else 0)
        # Обрабатываем каждый документ на странице
        # Если есть еще страницы, переходим на следующую
        self.logger.info(f'Текущий запрос: {response.url}')
        self.logger.info(f"По такому запросу найдено {doc_n} документов и {num_pages} страниц")
        for i in range(0, num_pages):
            next_start = i * self.doc_per_page
            next_url = self.change_start(response.url, next_start)
            yield scrapy.Request(next_url, callback=self.parse_doc_links)



    def parse_doc_links(self, response):
        docs_links = response.css('.l_link .bold::attr(href)').getall()
        for link in docs_links:
            doc_id = self.get_doc_id(self.start_urls[0] + link)
            yield scrapy.Request(self.start_urls[0] + f'?doc_itself=&nd={doc_id}&page=1&rdk=0&link_id=1&fulltext=1',
                                 callback=self.parse_doc,
                                 cb_kwargs={'doc_id': doc_id})

    def parse_doc(self, response, **kwargs):
        start_meta = True
        with open(Path('H:\Files\Projects\PythonProjects\PravoData\pravo_gov\data\html') / Path(f'{kwargs["doc_id"]}.html'), 'w', encoding='cp1251') as f:
            if not response.text:
                self.logger.warn(f'Документ {kwargs["doc_id"]} не был скачан, перезапуск')
                start_meta = False
                yield scrapy.Request(self.start_urls[0] + f'?doc_itself=&nd={kwargs["doc_id"]}&page=1&rdk=0&link_id=1&fulltext=1',
                                     callback=self.parse_doc,
                                     cb_kwargs={'doc_id': kwargs["doc_id"]})
            else:
                f.write(response.text)

        if start_meta:
            yield scrapy.Request(self.start_urls[0] + f'?doc_itself=&vkart=card&nd={kwargs["doc_id"]}&page=1&rdk=0&link_id=1',
                                 callback=self.parse_meta,
                                 cb_kwargs={'doc_id': kwargs["doc_id"]})

    def parse_meta(self, response, **kwargs):
        document = DocumentItem()
        document['id'] = kwargs['doc_id']
        document['status'] = response.css('.DC_status i::text').get()
        document['name'] = response.css('b::text').get()
        document['description'] = response.css('p::text').get()
        document['signature'] = response.css('#pd::text').get()
        document['publications'] = response.css('.tiny::text').getall()
        document['keywords'] = response.css('#klsl::text').get().split(',')
        document['branches'] = [row.css("td i::text, td:not(:first-child)::text").getall()
                for row in response.css("#rubr table tr")
                if row.css("td")]
        yield document



    def change_start(self, url, start):
        updated_url = re.sub(r'\bstart=\d+\b', f'start={start}', url)
        updated_url = updated_url.replace('searchlist', 'list_itself', 1) + '&page='
        return updated_url

    def get_doc_id(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        nd_param = query_params["nd"][0]
        return nd_param




