from http.client import responses
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'nce1'

    start_urls = ['https://en-nce.xiao84.com/nce1/19991.html']

    def parse(self, response):
        # /html/body/div[2]/div[1]/div/section[1]/div[1]/h1
        title = response.css('div.title>h1::text').get()
        print()
        print()
        print('title：')
        print(title)
        content = response.css('div.content')
        print()
        print()
        print('content:')
        print(content)
        text = ''
        for p in content.xpath('.//p/text()'):
            print()
            print()
            print('paragraph:')
            print(p.get())
            text += p.get()

        print()
        print()
        print('text:')
        print(text)

        with open("nce1.txt", 'a+') as f:
            f.write(title)
            f.write("\r\n")
            f.write(text)
            f.write("\r\n")
        
        pages = response.css('div.context>ul>li>a::attr(href)').getall()

        if len( pages ) > 0:
            next_page = pages[-1]
            next_page = response.urljoin(next_page)
            print()
            print()
            print('next_page')
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
 
        # author_page_links = response.css('.author + a')
        # yield from response.follow_all(author_page_links, self.parse_author)

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }