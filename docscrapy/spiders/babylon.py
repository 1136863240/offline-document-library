import scrapy
import os

class RustSpider(scrapy.Spider):
    name = 'babylon'
    allowed_domains = [
        'endoc.cnbabylon.com',
        'minio.cnbabylon.com',
        'cdn.bootcdn.net',
    ]
    start_urls = ['https://endoc.cnbabylon.com/api/']
    root_url = 'https://endoc.cnbabylon.com'
    std_url = 'https://endoc.cnbabylon.com/api/'
    inner_href = []
    css_index_list = []
    sub_index = 0
    css_i = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('babylon/css'):
            os.makedirs('babylon/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if css not in self.inner_href:
                print('item:', item)
                if item.startswith('https://'):
                    print('css https:', item)
                    yield scrapy.Request(item, self.css_parse)
                elif item.startswith('//'):
                    print('css //:', item)
                    yield scrapy.Request('https:%s' % item, self.css_parse)
                elif item.startswith('/'):
                    print('css /:', item)
                    yield scrapy.Request('%s%s' % (self.root_url, item), self.css_parse)
                else:
                    print('css:', item)
                    yield scrapy.Request('%s%s' % (self.std_url, item), self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(item, 'css/%s' % css)
                self.inner_href.append(css)
            else:
                html = html.replace(item, 'css/%s' % css)
        
        html_list = response.xpath('//a[@class="tsd-kind-icon"]/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        f = open('babylon/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        file_path = 'babylon/css/%s'
        if file_arr[0] == '..' or len(file_arr) == 3:
            parent_dir = response.url.replace('/' + file_arr[-1], '')
            if not os.path.exists('babylon/' + parent_dir):
                os.makedirs('babylon/' + parent_dir)
            filename = file_arr[-1]
            file_path = 'babylon/%s/%s' % (parent_dir, filename)
        filename = file_arr[len(file_arr) - 1]
        f = open(file_path % filename, 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        self.css_i += 1
        print('css_parse end...')
    
    def sub_parse(self, response):
        print('sub%d start...' % self.sub_index)
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if css not in self.inner_href:
                print('item:', item)
                if item.startswith('https://'):
                    print('css https:', item)
                    yield scrapy.Request(item, self.css_parse)
                elif item.startswith('//'):
                    print('css //:', item)
                    yield scrapy.Request('https:%s' % item, self.css_parse)
                elif item.startswith('/'):
                    print('css /:', item)
                    yield scrapy.Request('%s%s' % (self.root_url, item), self.css_parse)
                else:
                    print('css:', item)
                    yield scrapy.Request('%s%s' % (self.std_url, item), self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(item, 'css/%s' % css)
                self.inner_href.append(css)
            else:
                html = html.replace(item, 'css/%s' % css)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        url = response.url.replace(self.std_url, '')
        print('filename:', url)
        filename = url.split('/')[-1]
        parent_dir = url.replace(filename, '')

        if not os.path.exists('babylon/' + parent_dir):
            os.makedirs('babylon/' + parent_dir)
        f = open('babylon/%s' % url, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1

