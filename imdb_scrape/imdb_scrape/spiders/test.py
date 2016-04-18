from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from imdb_scrape.items import ImdbScrapeItem
from scrapy.http.request import Request

import csv

class MySpider(BaseSpider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    #start_urls = ["http://www.imdb.com/title/tt0109950/?ref_=fn_al_tt_1"]
    #start_urls = ["http://www.imdb.com/find?ref_=nv_sr_fn&q=/Toy Story (1995)"]
    #lines=[]
    movies=[]
    text_file = open("movies.dat", "r")
    lines = text_file.read().split('\n')
    l=[]
    for line in lines:
        line = line.split("::")
        l.append(line)
    #with open('Test.dat','r') as f:
    #   reader=csv.reader(f,delimiter=":")
    #    for line in reader:
    #        lines.append([l for l in line if l.strip() != ''])
    l = l[:3883]
    for line in l:
        movies.append(line[1])
    urls = []
    for movie in movies:
        urls.append("http://www.imdb.com/find?ref_=nv_sr_fn&q=/" + movie)
    start_urls = urls    
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        link = hxs.select("//div[@class='findSection']/table[@class='findList']/tr/td/a/@href").extract()[0]
        link = "http://www.imdb.com" + link
        yield Request(link, callback=self.parse_movies)
        
    def parse_movies(self, response):
        hxs = HtmlXPathSelector(response)
        rating = hxs.select("//span[@itemprop='ratingValue']/text()").extract()[0]
        cast = hxs.select('//table[@class="cast_list"]/tr/td[@itemprop="actor"]//text()').extract()
        cast = filter(None, self.trim_list(cast))
        director = hxs.select('//span[@itemprop="director"]/a/span[@itemprop="name"]/text()').extract()
        director = self.trim_list(director)
        movie_name = hxs.select('//div[@class="title_wrapper"]/h1[@itemprop="name"]/text()').extract()
        movie_name = filter(None, self.trim_list(movie_name))
        year = hxs.select('//span[@id="titleYear"]/a/text()').extract()
        year = self.trim_list(year)
        #print movie_name, year, rating, director, cast
        item = ImdbScrapeItem()
        item['movie_name'] = movie_name
        item['year'] = year
        item['rating'] = rating
        item['director'] = director
        item['cast'] = cast
        return item
        
    def trim(self, raw_str):
        """
        Removes unicode strings from given string. Utility function
        being invoked by multiple functions. Returned value has also
        been stripped.
        """
        return raw_str.encode('ascii', errors='ignore').strip()

    def trim_list(self, raw_list):
        """
        Given a list containing strings that have unicode parts, it
        returns a list having no unicode strings. List items have
        also been stripped.
        """
        return [self.trim(raw_str) for raw_str in raw_list]  

    def get_urls():
        lines=[]
        movies=[]
        with open('Movies.dat','r') as f:
            reader=csv.reader(f,delimiter=":")
            for line in reader:
                lines.append([l for l in line if l.strip() != ''])
        for line in lines:
            movies.append(line[1])
        urls = []
        for movie in movies:
            urls.append("http://www.imdb.com/find?ref_=nv_sr_fn&q=/" + movie)
        return urls         