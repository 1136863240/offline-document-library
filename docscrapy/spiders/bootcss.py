import scrapy
import os

class BootcssSpider(scrapy.Spider):
    name = 'bootcss'
    allowed_domains = ['v4.bootcss.com', 'cdn.jsdelivr.net']
    start_urls = [
        'https://v4.bootcss.com/docs/getting-started/introduction/',
        'https://v4.bootcss.com/docs/layout/overview/',
        'https://v4.bootcss.com/docs/content/reboot/',
        'https://v4.bootcss.com/docs/components/alerts/',
        'https://v4.bootcss.com/docs/utilities/borders/',
        'https://v4.bootcss.com/docs/extend/approach/',
        'https://v4.bootcss.com/docs/migration/',
    ]
    domain_name = 'https://v4.bootcss.com'
    css_target = []
    css_index_list = []
    html_list = []
    css_i = 0
    inner_href = []
    sub_index = 0

    def parse(self, response):
        print('main start...')
        print('url1:', response.url)

        current_filename = ''
        if response.url == 'https://v4.bootcss.com/docs/getting-started/introduction/':
            current_filename = 'index.html'
        else:
            url = response.url
            file_arr = url.split('/')
            filename = file_arr[len(file_arr) - 2] + '.html'
            current_filename = filename
        
        if not os.path.exists('bootcss'):
            os.mkdir('bootcss')
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        css_target = response.xpath('//link[@rel="stylesheet"]').extract()
        html = response.text
        for item in css_list:
            css_arr = item.split('?')
            item = css_arr[0]
            if item not in self.inner_href:
                txt = item
                if item.find('/', 0) == 0:
                    item = self.domain_name + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(css_target[i], '<link href="css/css%d.css" rel="stylesheet">' % i)
                self.inner_href.append(txt)
            else:
                i = self.inner_href.index(item)
                html = html.replace(css_target[i], '<link href="css/css%d.css" rel="stylesheet">' % i)
        
        html_list = response.xpath('//nav[@class="bd-links"]/div[contains(@class, "active")]/ul/li[not(contains(@class, "active"))]/a/@href').extract()
        sub_html_index = 0
        for item in html_list:
            url = '%s%s' % (self.domain_name, item)
            yield scrapy.Request(url, self.sub_parse)
            file_arr = url.split('/')
            filename = file_arr[len(file_arr) - 2] + '.html'
            html = html.replace(item, filename)
            sub_html_index += 1
        
        filename = ''
        active_link = response.xpath('//nav[@class="bd-links"]/div[contains(@class, "active")]/ul/li[contains(@class, "active")]/a/@href').extract()
        for item in active_link:
            if item == '/docs/getting-started/introduction/':
                filename = 'index.html'
                html = html.replace(item, filename)
            else:
                url = '%s%s' % (self.domain_name, item)
                file_arr = url.split('/')
                filename = file_arr[len(file_arr) - 2] + '.html'
                html = html.replace(item, filename)

        other_link = response.xpath('//nav[@class="bd-links"]/div[not(contains(@class, "active"))]/a/@href').extract()
        for item in other_link:
            print('item:', item)
            if item == '/docs/getting-started/introduction/':
                filename = 'index.html'
                html = html.replace(item, filename)
            else:
                url = '%s%s' % (self.domain_name, item)
                file_arr = url.split('/')
                filename = file_arr[len(file_arr) - 2] + '.html'
                html = html.replace(item, filename)

        f = open('bootcss/%s' % current_filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        if not os.path.exists('bootcss/css'):
            os.makedirs('bootcss/css')
        
        f = open('bootcss/css/css%d.css' % self.css_index_list[self.css_i], 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        self.css_i += 1
        print('css_parse end...')
    
    def sub_parse(self, response):
        print('sub%d start...' % self.sub_index)
        print('url2:', response.url)
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        css_target = response.xpath('//link[@rel="stylesheet"]').extract()
        html = response.text
        for item in css_list:
            css_arr = item.split('?')
            item = css_arr[0]
            if item not in self.inner_href:
                txt = item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(css_target[i], '<link href="css/css%d.css" rel="stylesheet">' % i)
                self.inner_href.append(txt)
            else:
                i = self.inner_href.index(item)
                html = html.replace(css_target[i], '<link href="css/css%d.css" rel="stylesheet">' % i)

        other_link = response.xpath('//nav[@class="bd-links"]/div[not(contains(@class, "active"))]/a/@href').extract()
        for item in other_link:
            if item == '/docs/getting-started/introduction/':
                filename = 'index.html'
                html = html.replace(item, filename)
            else:
                url = '%s%s' % (self.domain_name, item)
                file_arr = url.split('/')
                filename = file_arr[len(file_arr) - 2] + '.html'
                html = html.replace(item, filename)

        index = 1
        file_arr = response.url.split('/')
        current_filename = file_arr[len(file_arr) - 2] + '.html'
        print('filename:', current_filename)
        
        html_list = response.xpath('//nav[@class="bd-links"]/div[contains(@class, "active")]/ul/li[not(contains(@class, "active"))]/a/@href').extract()
        sub_html_index = 0
        filename = ''
        for item in html_list:
            if item == '/docs/getting-started/introduction/':
                html = html.replace(item, 'index.html')
            else:
                url = '%s%s' % (self.domain_name, item)
                file_arr = url.split('/')
                index = 1
                filename = file_arr[len(file_arr) - index]
                while filename == '':
                    index += 1
                    filename = file_arr[len(file_arr) - index]
                filename += '.html'
                html = html.replace(item, filename)
                sub_html_index += 1
        
        active_link = response.xpath('//nav[@class="bd-links"]/div[contains(@class, "active")]/ul/li[contains(@class, "active")]/a/@href').extract()
        for item in active_link:
            html = html.replace(item, current_filename)

        f = open('bootcss/%s' % current_filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1
