import scrapy
from pyquery import PyQuery as pq
import os


class ElectronjsSpider(scrapy.Spider):
    name = 'electronjs'
    allowed_domains = [
        'www.electronjs.org'
    ]
    start_urls = ['https://www.electronjs.org/docs']
    inner_href = []
    css_files = []

    def parse(self, response):
        if not os.path.exists('electronjs/css'):
            os.makedirs('electronjs/css')
        
        print('main start...')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for css in css_list:
            css_arr = css.split('/')
            css_filename = css_arr[len(css_arr) - 1]
            if css not in self.inner_href:
                self.inner_href.append(css)
                self.css_files.append(css_filename)
                html = html.replace(css, 'css/%s' % css_filename)
                if css.find('/', 0) == 0:
                    css_url = 'https://www.electronjs.org%s' % css
                    yield scrapy.Request(css_url, self.css_parse)
                else:
                    yield scrapy.Request(css, self.css_parse)
            else:
                html = html.replace(css, 'electronjs/css/%s' % css_filename)
        
        sub_list1 = response.xpath('//div[contains(@class, "docs-guides-list")]//a/@href').extract()
        for item in sub_list1:
            url = 'https://www.electronjs.org%s' % item
            html = html.replace(item, item[1:] + '.html')
            yield scrapy.Request(url, self.sub_parse)
        sub_list2 = response.xpath('//div[contains(@class, "d-sm-flex")]//ul//a/@href').extract()
        for item in sub_list2:
            url = 'https://www.electronjs.org%s' % item
            html = html.replace(item, item[1:] + '.html')
            yield scrapy.Request(url, self.sub_parse)
        
        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')

        main_file = open('electronjs/index.html', 'w', encoding='utf-8')
        main_file.write(html)
        main_file.flush()
        main_file.close()
        print('main stop...')
    
    def css_parse(self, response):
        print('css start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('electronjs/css/%s' % filename, 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        print('css stop...')
    
    def sub_parse(self, response):
        current_url_path = response.url.replace('https://www.electronjs.org/', '')
        path_arr = current_url_path.split('/')
        filename = path_arr[len(path_arr) - 1]
        current_url_path = current_url_path.replace(filename, '')
        if not os.path.exists('electronjs/' + current_url_path):
            os.makedirs('electronjs/' + current_url_path)
        print('sub start...')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for css in css_list:
            css_temp = css
            css_arr = css.split('/')
            css_filename = css_arr[len(css_arr) - 1]
            css_temp = css_temp.replace('/' + css_filename, '')
            css_deep = len(css_temp.split('/'))
            parent = ''
            for i in range(css_deep):
                parent += '../'
            if css not in self.inner_href:
                self.inner_href.append(css)
                self.css_files.append(css_filename)
                html = html.replace(css, '%scss/%s' % (parent, css_filename))
                if css.find('/', 0) == 0:
                    css_url = 'https://www.electronjs.org%s' % css
                    yield scrapy.Request(css_url, self.css_parse)
                else:
                    yield scrapy.Request(css, self.css_parse)
            else:
                html = html.replace(css, '%scss/%s' % (parent, css_filename))
        
        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        f = open('electronjs/' + current_url_path + filename + '.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub stop...')
