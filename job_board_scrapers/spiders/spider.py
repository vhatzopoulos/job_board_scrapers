import scrapy
from urllib.parse import urljoin

class MonsterSpider(scrapy.Spider):
    name = "monster"

    def start_requests(self):

        first_page = 1
        last_page = 2
        start_url = 'https://www.monster.co.uk/jobs/search/Contract_8?cy=uk&page='
        urls = [start_url + str(i) for i in range(first_page, last_page + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        page = response.url.split('&')[1]
        filename = 'monster-contractor-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        '''
        '''
        for job in response.css('div.jobTitle'):
            yield {
                'add_url': job.css("h2 a::attr(href)").extract()[0]
            }
        '''
        # follow links to job details page
        for href in response.css("div.jobTitle h2 a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

    def parse_job_details(self, response):
        pass

# scrapy shell 'https://www.monster.co.uk/jobs/search/Contract_8?cy=uk&page='
# response.xpath('//div[@class="jobTitle"] /h2/a/@href').extract()
# job = response.css("div.jobTitle")
# job.css("h2 a::attr(href)").extract()[0]


class ReedSpider(scrapy.Spider):
    name = "reed"
    '''
    def start_requests(self):

        urls = ['https://www.reed.co.uk/jobs/contract']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    '''
    start_urls = ['https://www.reed.co.uk/jobs/contract']

    def parse(self, response):
        # follow links to job details page
        for href in response.css("h3.title a::attr(href)").extract():
            #print(href)
            #input()
            href = 'https://www.reed.co.uk' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)
        
        # follow pagination links
        next_page = response.css('div.pages a::attr(href)').extract()[-1]
        next_page = 'https://www.reed.co.uk' + next_page
        #print(next_page)
        #input()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'name': extract_with_css('header.job-header h1::text'),
            'salary': response.css("div.metadata ul li.salary::text").extract()[-1].strip(),
            'time': response.css("div.metadata ul li.time::text").extract()[-1].strip(),
            'skills': ','.join(response.css("div.skills ul li.skill-name::text").extract())
        }


class IndeedSpider(scrapy.Spider):
    name = "indeed"

    def start_requests(self):

        first_page = 1
        last_page = 2
        start_url = 'https://www.indeed.co.uk/jobs?q=&l=uk&jt=contract&start=0'
        urls = [start_url + str(i) for i in range(first_page, last_page + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('&')[-1]
        filename = "indeed"+'-contractor-adds-page-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


