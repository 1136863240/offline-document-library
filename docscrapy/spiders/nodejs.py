import scrapy
import os

class NodejsSpider(scrapy.Spider):
    name = 'nodejs'
    allowed_domains = ['nodejs.cn', 'static.nodejs.cn']
    start_urls = ['http://nodejs.cn/api/']
    inner_href = []
    css_index_list = []
    sub_index = 0
    css_i = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('nodejs/css'):
            os.makedirs('nodejs/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                if item.find('//', 0) == 0:
                    item = 'http:' + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(txt)
            else:
                html = html.replace(item, 'css/%s' % css)
        
        html_list = response.xpath('//div[@id="apicontent"]/ul/li/a/@href').extract()
        for item in html_list:
            yield scrapy.Request('%s%s' % (self.start_urls[0], item), self.sub_parse)

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')

        f = open('nodejs/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('nodejs/css/%s' % filename, 'w', encoding='utf-8')
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
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                if item.find('//', 0) == 0:
                    item = 'http:' + item
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
        
        apicontent = response.xpath('//div[@id="apicontent"]//a/@href').extract()
        for item in apicontent:
            rep = item.replace('/api/', '')
            html = html.replace(item, rep)

        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        print('filename:', filename)

        f = open('nodejs/%s' % filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1
