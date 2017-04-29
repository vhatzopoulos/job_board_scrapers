import scrapy
from datetime import datetime, timedelta


class ReedSpider(scrapy.Spider):
    name = "reed"
    start_urls = ['https://www.reed.co.uk/jobs/education?contract=True', 'https://www.reed.co.uk/jobs/it-jobs?contract=True', 'https://www.reed.co.uk/jobs/health-jobs?contract=True', 'https://www.reed.co.uk/jobs/construction-property?contract=True', 'https://www.reed.co.uk/jobs/admin-secretarial-pa?contract=True','https://www.reed.co.uk/jobs/logistics?contract=True', 'https://www.reed.co.uk/jobs/social-care?contract=True', 'https://www.reed.co.uk/jobs/engineering?contract=True', 'https://www.reed.co.uk/jobs/accountancy?contract=True', 'https://www.reed.co.uk/jobs/hr-jobs?contract=True', 'https://www.reed.co.uk/jobs/accountancy-qualified?contract=True', 'https://www.reed.co.uk/jobs/marketing?contract=True', 'https://www.reed.co.uk/jobs/customer-service?contract=True','https://www.reed.co.uk/jobs/factory?contract=True', 'https://www.reed.co.uk/jobs/catering-jobs?contract=True', 'https://www.reed.co.uk/jobs/sales?contract=True', 'https://www.reed.co.uk/jobs/finance?contract=True', 'https://www.reed.co.uk/jobs/law?contract=True', 'https://www.reed.co.uk/jobs/banking?contract=True', 'https://www.reed.co.uk/jobs/media-digital-creative?contract=True', 'https://www.reed.co.uk/jobs/science?contract=True', 'https://www.reed.co.uk/jobs/purchasing?contract=True', 'https://www.reed.co.uk/jobs/retail?contract=True', 'https://www.reed.co.uk/jobs/motoring-automotive?contract=True', 'https://www.reed.co.uk/jobs/strategy-consultancy?contract=True', 'https://www.reed.co.uk/jobs/charity?contract=True', 'https://www.reed.co.uk/jobs/graduate-training-internships?contract=True', 'https://www.reed.co.uk/jobs/security-safety?contract=True', 'https://www.reed.co.uk/jobs/fmcg?contract=True', 'https://www.reed.co.uk/jobs/recruitment-consultancy?contract=True', 'https://www.reed.co.uk/jobs/leisure-tourism?contract=True', 'https://www.reed.co.uk/jobs/energy?contract=True', 'https://www.reed.co.uk/jobs/general-insurance?contract=True', 'https://www.reed.co.uk/jobs/training?contract=True', 'https://www.reed.co.uk/jobs/estate-agent?contract=True', 'https://www.reed.co.uk/jobs/apprenticeships?contract=True', 'https://www.reed.co.uk/jobs/other?contract=True']

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
            'skills': ','.join(response.css("div.skills ul li.skill-name::text").extract()),
            'sector': response.css("ul.breadcrumbs a::text").extract_first(),
            'posted': response.css("meta[itemprop=datePosted]::attr(datetime)").extract_first()
        }

class IndeedSpider(scrapy.Spider):
    
    name = "indeed"
    start_urls = ['https://www.indeed.co.uk/jobs?q=Accounting&jt=contract']

    def parse(self, response):
        # follow links to job details page
        for href in response.css("a.jobtitle::attr(href)").extract():
            href = 'https://www.indeed.co.uk' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css("div.pagination a::attr(href)")[-1].extract()
        next_page = 'https://www.indeed.co.uk' + next_page

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        def parse_date(time_ago_posted_string):
            #how many hours or days was the job posted?
            time_ago_posted = [int(s) for s in time_ago_posted_string.split() if s.isdigit()][0]
            if 'day' in time_ago_posted or 'days' in time_ago_posted:
                date_posted = datetime.now() - timedelta(days=time_ago_posted)
            if 'hour' in time_ago_posted or 'hours' in time_ago_posted:
                date_posted = datetime.now() - timedelta(hours=time_ago_posted)
            return date_posted

        yield {
            'name': response.css("b.jobtitle font::text").extract_first(),
            'company': response.css("span.company::text").extract_first(),
            'location': response.css("span.location::text").extract_first(),
            'salary': response.css('span[style="white-space: nowrap"]::Text').extract_first(),
            'sector': response.css("ul.breadcrumbs a::text").extract_first(),
            'posted': parse_date(response.css("div.result-link-bar-container span.date::text").extract_first())
        }


class totalJobsSpider(scrapy.Spider):
    name = "totaljobs"
    sectors = ['accountancy','administration', 'advertising', 'aerospace', 'apprenticeship','automotive', 'banking', 'call-centre', 'catering', 'charity', 'civil-service', 'construction', 'creative', 'customer-service', 'digital', 'education', 'engineering', 'finance', 'fmcg', 'graduate', 'healthcare', 'hospitality', 'hr', 'insurance', 'it', 'legal', 'leisure', 'logistics', 'management-consultancy', 'manufacturing', 'marketing', 'media', 'nursing', 'oil-and-gas', 'pa', 'part-time', 'pharmaceuticals', 'pr', 'property', 'public-sector', 'recruitment-sales', 'renewable-energy', 'retail', 'sales', 'science', 'secretarial', 'senior-appointments', 'social-work', 'teaching', 'telecoms', 'temporary', 'tourism', 'transport', 'travel', 'utilities', 'wholesale'] 
    start_urls = ['https://www.totaljobs.com/jobs/contract/' + sector for sector in sectors]

    def parse(self, response):
        # follow links to job details page
        for href in response.css("div.job-title a::attr(href)").extract():
            href = 'https://www.totaljobs.com' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = response.css('a.next::attr(href)').extract()[-1]
        next_page = response.url + next_page

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

    def parse(self, response, start_urls=start_urls):
        # follow links to job details page
        for href in response.css("meta[property=url]::attr(content)").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        # follow pagination links
        next_page = start_urls[0] + response.css("a.next::attr(href)").extract()[0]
        next_page = response.css("a.next::attr(href)").extract()[0]
        
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):

        location ='N/A'
        try:
            location = response.css("meta[property=addressLocality]::attr(content)").extract()[0] +', ' +response.css("meta[property=addressRegion]::attr(content)").extract()[0]
        except IndexError:
            pass

        yield {
            'job_title': response.css("h1::text").extract()[0].strip(),
            'location':  location,
            'salary': response.css("div[property=baseSalary]::text").extract_first(),
            'hiringOrganization': response.css("div[property=hiringOrganization] meta[property=name]::attr(content)").extract_first(),
            'date_posted':  response.css("meta[property=datePosted]::attr(content)").extract_first()


        }



class fish4Spider(scrapy.Spider):
    name = "fish4"
    start_urls = ['http://www.fish4.co.uk/jobs/contract/#browsing']

    def parse(self, response, start_urls=start_urls):
        # follow links to job details page
        for href in response.css("a.js-clickable-area-link::attr(href)").extract():
            href = 'http://www.fish4.co.uk' + href
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

        #follow pagination links
        next_page = response.css("a[rel=next]::attr(href)").extract()[0]
        next_page = 'http://www.fish4.co.uk' + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_details(self, response):

        keys = response.css("dt.grid-item.two-fifths.portable-one-whole.palm-one-half::text").extract()
        keys = list(map( lambda item :item.strip(), keys))
        values = response.css("dd.grid-item.three-fifths.portable-one-whole.palm-one-half::text").extract()
        values = list(map( lambda item :item.strip(), values))

        yield dict(zip(keys, values))




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

        try:
            name = response.css("span.title h1::text").extract()[0].strip()
        except IndexError:
            name = 'N/A'

        try:
            addressLocality = response.css("span.locationConcat::text").extract()[0]
        except IndexError:
            addressLocality = 'N/A'

        try:
            salary = response.css("span.salary::text").extract()[0].strip()
        except IndexError:
            salary = 'N/A'

        try:
            jobType = response.css("span.jobType::text").extract()[0]
        except IndexError:
            jobType = 'N/A'

        yield {
            'name': name,
            'addressLocality': addressLocality,
            'salary': salary,
            'jobType': jobType
            }


########################## junk ##########################
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
       
        # follow links to job details page
        for href in response.css("div.jobTitle h2 a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)

    def parse_job_details(self, response):
        pass

# return 204 on get request
class cvLibrarySpider(scrapy.Spider):
    name = "cvlibrary"
    start_urls = ['https://www.cv-library.co.uk/search-jobs?search=1&q=&geo=&distance=15&salarymin=&salarymax=&salarytype=annum&posted=28&industry=25&tempperm=Contract']

    def parse(self, response, start_urls=start_urls):
        # follow links to job details page
        for href in response.css("div.a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_job_details)