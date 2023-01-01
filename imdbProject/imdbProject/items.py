import scrapy
from abc import ABC

class IMDBItem(scrapy.Item, ABC):
    titre = scrapy.Field()
    titre_original = scrapy.Field()
    score = scrapy.Field()
    genre = scrapy.Field()
    date = scrapy.Field()
    duree = scrapy.Field()
    descriptions = scrapy.Field()
    acteurs = scrapy.Field()
    public = scrapy.Field()
    pays = scrapy.Field()
    langue_origine = scrapy.Field()
    isFilm = scrapy.Field()
    

    

class filmItem(IMDBItem):
    pass

class serieItem(IMDBItem):
    nbSaisons = scrapy.Field()
    nbEpisodes = scrapy.Field()
