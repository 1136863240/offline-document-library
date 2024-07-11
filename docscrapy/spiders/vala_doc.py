import scrapy
import os

class RustSpider(scrapy.Spider):
    name = 'vala_doc'
    allowed_domains = ['valadoc.org']
    start_urls = ['https://valadoc.org/']
    root_url = 'https://valadoc.org'
    std_url = 'https://valadoc.org'
    inner_href = []
    css_index_list = []
    sub_index = 0
    css_i = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('vala_doc/css'):
            os.makedirs('vala_doc/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        print('css:')
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[-1]
            if css not in self.inner_href:
                txt = item
                item = self.std_url + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(css)
            else:
                html = html.replace(item, 'css/%s' % css)
        
        html_list = response.xpath('//div[@class="site_navigation"]/a/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            i = item
            if item[0] == '/':
                i = i[1:]
            html = html.replace(item, i)
        
        html_list = response.xpath('//a[@class="package"]/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            i = item
            if i[0] == '/':
                i = i[1:]
            html = html.replace(item, i)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        f = open('vala_doc/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[-1]
        f = open('vala_doc/css/%s' % filename, 'w', encoding='utf-8')
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
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[-1]
            item_arr = item.split('/')
            line_len = len(item_arr) - 2
            dot = ''
            if line_len > 0:
                for i in range(line_len):
                    dot += '../'
            if item not in self.inner_href:
                txt = item
                item = self.std_url + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, f'{dot}css/{css}')
                self.inner_href.append(txt)
            else:
                html = html.replace(item, f'{dot}css/{css}')
        
        html_list = response.xpath('//ul[@class="navi_inline"]/li/a/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.content_parse)
            i = item
            if i[0] == '/':
                i = f'..{i}'
            html = html.replace(item, i)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')
        
        file_arr = response.url.split('/')
        filename = file_arr[-1]
        print('filename:', filename)
        _dir = response.url.replace(self.std_url, '').replace(filename, '')
        if _dir[0] == '/':
            _dir = _dir[1:]
        if _dir[-1] == '/':
            _dir = _dir[:-1]
        print(f'sub _dir:{_dir}')
        if not os.path.exists(f'vala_doc/{_dir}'):
            os.makedirs(f'vala_doc/{_dir}')

        f = open('vala_doc/%s/%s' % (_dir, filename), 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1
    
    def content_parse(self, response):
        print('content%d start...' % self.sub_index)
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[-1]
            item_arr = item.split('/')
            line_len = len(item_arr) - 2
            dot = ''
            if line_len > 0:
                for i in range(line_len):
                    dot += '../'
            if item not in self.inner_href:
                txt = item
                item = self.std_url + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, f'{dot}css/{css}')
                self.inner_href.append(txt)
            else:
                html = html.replace(item, f'{dot}css/{css}')
        
        html_list = response.xpath('//ul[@class="navi_inline"]/li/a/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.info_parse)
            i = item
            if i[0] == '/':
                i = f'..{i}'
            html = html.replace(item, i)
        
        html_list = response.xpath('//ul[@class="navi_inline"]/li/span/b/a/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.info_parse)
            i = item
            if i[0] == '/':
                i = f'..{i}'
            html = html.replace(item, i)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')
        
        file_arr = response.url.split('/')
        filename = file_arr[-1]
        print('filename:', filename)
        _dir = response.url.replace(self.std_url, '').replace(filename, '')
        if _dir[0] == '/':
            _dir = _dir[1:]
        if _dir[-1] == '/':
            _dir = _dir[:-1]
        print(f'content _dir:{_dir}')
        if not os.path.exists(f'vala_doc/{_dir}'):
            os.makedirs(f'vala_doc/{_dir}')

        f = open('vala_doc/%s/%s' % (_dir, filename), 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('content%d end...' % self.sub_index)
        self.sub_index += 1
    
    def info_parse(self, response):
        print('info%d start...' % self.sub_index)
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[-1]
            item_arr = item.split('/')
            line_len = len(item_arr) - 2
            dot = ''
            if line_len > 0:
                for i in range(line_len):
                    dot += '../'
            if item not in self.inner_href:
                txt = item
                item = self.std_url + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, f'{dot}css/{css}')
                self.inner_href.append(txt)
            else:
                html = html.replace(item, f'{dot}css/{css}')
        
        file_arr = response.url.split('/')
        filename = file_arr[-1]
        print('filename:', filename)
        _dir = response.url.replace(self.std_url, '').replace(filename, '')
        if _dir[0] == '/':
            _dir = _dir[1:]
        if _dir[-1] == '/':
            _dir = _dir[:-1]
        print(f'info _dir:{_dir}')
        if not os.path.exists(f'vala_doc/{_dir}'):
            os.makedirs(f'vala_doc/{_dir}')

        f = open('vala_doc/%s/%s' % (_dir, filename), 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('info%d end...' % self.sub_index)
        self.sub_index += 1

