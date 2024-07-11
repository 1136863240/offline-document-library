import scrapy
import os

class RustNcursesSpider(scrapy.Spider):
    name = 'rust_ncurses'
    allowed_domains = ['docs.rs']
    start_urls = ['https://docs.rs/ncurses/latest/ncurses/index.html']
    root_url = 'https://docs.rs'
    sub_url = 'https://docs.rs/ncurses/latest/ncurses/'
    constants_url = 'https://docs.rs/ncurses/latest/ncurses/constants/'
    inner_href = []
    css_index_list = []
    sub_index = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('rust-ncurses/css'):
            os.makedirs('rust-ncurses/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                yield scrapy.Request('%s%s' % (self.root_url, item), self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(txt)
            else:
                html = html.replace(item, 'css/%s' % css)
        
        html_list = response.xpath('//a[@class="fn"]/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.sub_url, item), self.sub_parse)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        yield scrapy.Request('%s%s' % (self.constants_url, 'index.html'), self.constants_parse)

        f = open('rust-ncurses/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')

    def constants_parse(self, response):
        print('constants start...')
        if not os.path.exists('rust-ncurses/constants/css'):
            os.makedirs('rust-ncurses/constants/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                yield scrapy.Request('%s%s' % (self.constants_url, item), self.sub_css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, '../css/%s' % css)
                self.inner_href.append(txt)
            else:
                html = html.replace(item, '../css/%s' % css)
        
        html_list = response.xpath('//a[@class="fn"]/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.constants_url, item), self.sub_constants_parse)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        f = open('rust-ncurses/constants/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('constants end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('rust-ncurses/css/%s' % filename, 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        print('css_parse end...')
    
    def sub_css_parse(self, response):
        print('sub_css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('rust-ncurses/constants/css/%s' % filename, 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        print('sub_css_parse end...')
    
    def sub_parse(self, response):
        print('sub%d start...' % self.sub_index)
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                if item.find('..', 0) == 0:
                    item = self.root_url + item.split('/')[2]
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(txt)
            else:
                html = html.replace(item, 'css/%s' % css)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')
        
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        print('filename:', filename)

        f = open('rust-ncurses/%s' % filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1
    
    def sub_constants_parse(self, response):
        print('sub%d start...' % self.sub_index)
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                if item.find('..', 0) == 0:
                    item = self.root_url + item.split('/')[2]
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(txt)
            else:
                html = html.replace(item, 'css/%s' % css)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')
        
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        print('filename:', filename)

        f = open('rust-ncurses/constants/%s' % filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1
