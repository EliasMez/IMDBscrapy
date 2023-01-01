from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import filmItem, serieItem


class IMDBSpider(CrawlSpider):
    name = 'IMDB'
    allowed_domains = ['www.imdb.com']
    url_films = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    url_series = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
    start_urls = [url_films,url_series]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    rules = [(
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=False)  
    )]

    custom_settings = {
    'FEED_EXPORT_FIELDS': ["titre","titre_original","date","duree","descriptions","genre","langue_origine","pays","public","score","acteurs","nbSaisons","nbEpisodes"],
    # 'FEED_EXPORT_FIELDS': ["titre","duree"],

    'ITEM_PIPELINES': {
        'imdbProject.pipelines.ImdbPipeline': 300
    }
    }

    lang = 'fr'

    # atribut defini pour les test
    limit=15

    def parse_item(self, response):
        items_serie = serieItem()
        items_film = filmItem()
        
        # A décommenter pour limiter le nombre de liens scrappés au nombre défini par l'attribut limit
        # scrape_count = self.crawler.stats.get_value('item_scraped_count')
        # if scrape_count == self.limit:
        #     raise CloseSpider("Limit Reached")

        if 'top&ref' in response.request.url:
            items = items_film
            items['isFilm'] = 1

        elif 'toptv&ref' in response.request.url:
            items = items_serie
            items['isFilm'] = 0

            nb_saisons_path = '//select[@id="browse-episodes-season"]/@aria-label'
            items['nbSaisons'] = response.xpath(nb_saisons_path).extract_first()
            if not items['nbSaisons']:
                nb_saisons_path = '//a[contains(@href,"episodes?season")]/div/text()'
                items['nbSaisons'] = response.xpath(nb_saisons_path).extract_first()
            if not items['nbSaisons']:
                items['nbSaisons'] = "0"
            items['nbSaisons'] = int("".join([char for char in items['nbSaisons'] if char.isdigit()]))
            
            nb_episodes_path = '//a[contains(@href,"episodes")]/h3/span [@class="ipc-title__subtext"]/text()'
            items['nbEpisodes'] = int(response.xpath(nb_episodes_path).extract_first())
            

        titre = response.xpath('//h1[@class="sc-b73cd867-0 eKrKux"]/text()')
        sup_titre = response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').extract_first()
        items['titre'] = response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').extract_first()


        items['titre_original'] = response.xpath('//div[@data-testid="hero-title-block__original-title"]/text()').extract_first()
        if not items['titre_original'] :
            items['titre_original'] = items['titre']
        else :
            items['titre_original'] = items['titre_original'].split(': ')[-1]


        items['score'] = float(response.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()').extract_first().replace(',','.'))
        items['genre'] = response.xpath('//a/span[@class="ipc-chip__text"]/text()').extract()


        public_path = '//a[contains(@href,"parentalguide/certificates?ref_=tt_ov_pg")]/text()'
        items['public'] = response.xpath(public_path).extract()
        if not items['public']:
            items['public'] = "Non Renseigné"


        date_path = "//a[contains(@href,'releaseinfo?ref_=tt_dt_rdat')][@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']/text()"
        items['date'] = response.xpath(date_path).extract_first().split(' (')[0]


        duree = response.xpath('//div[@class="ipc-metadata-list-item__content-container"]/text()').extract()
        if len(duree) == 0:
            items['duree'] = 0
        elif len(duree) == 7:
            items['duree'] = int(duree[0])*60+int(duree[4])
        else :
            if duree[-1] == "minutes" :
                items['duree'] = int(duree[0])
            else :
                items['duree'] = int(duree[0])*60

    
        items['descriptions'] = response.xpath('//span[@class="sc-16ede01-1 kgphFu"]/text()').extract_first()
        items['acteurs'] = response.xpath('//a[@data-testid="title-cast-item__actor"]/text()').extract()

        items['pays'] = response.xpath('//a[contains(@href,"country_of_origin")]/text()').extract()

        langue_path = '//li[@data-testid="title-details-languages"]/div/ul/li/a/text()'
        items['langue_origine'] = response.xpath(langue_path).extract()
        items['langue_origine'] = [w.replace('Aucun','Muet') if w=='Aucun' else w for w in items['langue_origine']]
        
        yield items


# scrapy runspider nom_spider.py
# scrapy crawl nom_du_spider [-o(append), -O(overried)] saved_file.csv
# [extract(),extract_first()](none si vide) [get(),getall()](erreur si vide)
# scrapy genspider -l
# scrapy genspider -t crawl nom_creation_spider nom_url
# scrapy crawl nom_spider