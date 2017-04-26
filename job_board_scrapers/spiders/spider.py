import scrapy
from datetime import datetime, timedelta

class MonsterSpider(scrapy.Spider):
    name = "monster"

    def start_requests(self):

        first_page = 1
        last_page = 2
        start_urls = 'https://www.monster.co.uk/jobs/search/Contract_8?cy=uk&page='
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

class ReedSpider(scrapy.Spider):
    name = "reed"
    start_urls = ['https://www.reed.co.uk/jobs/contract']

    def parse(self, response):
        # follow links to job details page
        for href in response.css("h3.title a::attr(href)").extract():
            href = 'https://www.reed.co.uk' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css('div.pages a::attr(href)').extract()[-1]
        next_page = 'https://www.reed.co.uk' + next_page

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

class totalJobsSpider(scrapy.Spider):
    name = "totaljobs"
    sectors = ['accountancy','administration', 'advertising']
    start_urls = ['https://www.totaljobs.com/jobs/contract/'+sectors[0]]

    def parse(self, response):
        # follow links to job details page
        for href in response.css("div.job-title a::attr(href)").extract():
            href = 'https://www.totaljobs.com' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css('a.next::attr(href)').extract()[-1]
        next_page = 'https://www.totaljobs.com/jobs/contract/' + sectors[0] + next_page

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'name': response.css("h1::text").extract()[0].strip(),
            'addressLocality': response.css("meta[property=addressLocality]::attr(content)").extract()[0],
            'salary': response.css("div[property=baseSalary]::text").extract()[0],
            #'employmentType': response.css("div[property=employmentType]::text").extract()[0],
            'hiringOrganization': response.css("div[property=hiringOrganization] a::text").extract()[0]
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
        filename = "indeed" + '-contractor-adds-page-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

class CareerBuilderSpider(scrapy.Spider):
    name = "careerbuilder"
    start_urls = ['http://www.careerbuilder.com/jobs?emp=jtct&pay=20']


    def parse(self, response):
        # follow links to job details page
        for href in response.css("h2.job-title a::attr(href)").extract():
            href = 'http://www.careerbuilder.com' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css("a[id=next-button]::attr(href)").extract()[0]
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        date_posted = response.css("h3[id=job-begin-date]::text").extract()[0].strip()
        #how many hours or days was the job posted?
        time_ago_posted = [int(s) for s in date_posted.split() if s.isdigit()][0]
        if 'day' in date_posted or 'days' in date_posted:
            datePosted = datetime.now() - timedelta(days=time_ago_posted)
        if 'hour' in date_posted or 'hours' in date_posted:
            datePosted = datetime.now() - timedelta(hours=time_ago_posted)

        datePosted = str(datePosted.date())
        yield {
            'name': response.css("h1::text").extract()[0].strip(),
            'jobFacts': list(map(lambda item: item.strip(), response.css("div.tag::text").extract())),       
            'hiringOrganization': response.css("h2[id=job-company-name]::text").extract()[0].strip(),
            'datePosted': datePosted
        }

class cwJobsSpider(scrapy.Spider):
    name = "cwjobs"
    start_urls = ['https://www.cwjobs.co.uk/jobs/contract/']


class cvLibrarySpider(scrapy.Spider):
    name = "cvlibrary"
    start_urls = ['']

class jobsiteSpider(scrapy.Spider):
    name = "jobsite"
    start_urls = ['http://www.jobsite.co.uk/vacancies?search_type=advanced&vacancy_type=Contract']

    def parse(self, response):
        # follow links to job details page
        for href in response.css("div.clearfix h3 a::attr(href)").extract():
            href = 'http://www.jobsite.co.uk' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css("div.resultsPagination a::attr(href)").extract()[-1]
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'name': response.css("span.title h1::text").extract()[0].strip(),
            'addressLocality': response.css("span.locationConcat::text").extract()[0],
            'salary': response.css("span.salary::text").extract()[0].strip(),
            'jobType': response.css("span.jobType::text").extract()[0]
            }



