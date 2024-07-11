import scrapy
import os

class RustSpider(scrapy.Spider):
    name = 'thirtyfour_sync'
    allowed_domains = ['docs.rs']
    start_urls = ['https://docs.rs/thirtyfour_sync/0.27.1/thirtyfour_sync/all.html']
    root_url = 'https://docs.rs'
    std_url = 'https://docs.rs/thirtyfour_sync/0.27.1/thirtyfour_sync/'
    inner_href = []
    css_index_list = []
    sub_index = 0
    css_i = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('thirtyfour_sync/css'):
            os.makedirs('thirtyfour_sync/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if css not in self.inner_href:
                txt = item
                #if item.find('..', 0) == 0:
                #    item = self.root_url + item.split('/')[1]
                item = self.root_url + item
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(css)
            else:
                html = html.replace(item, 'css/%s' % css)
        
        html_list0 = response.xpath('//ul[@class="structs docblock"]/li/a/@href').extract()
        for item in html_list0:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])
        
        html_list1 = response.xpath('//ul[@class="enums docblock"]/li/a/@href').extract()
        for item in html_list1:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])
        
        html_list2 = response.xpath('//ul[@class="traits docblock"]/li/a/@href').extract()
        for item in html_list2:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])
      
        html_list6 = response.xpath('//ul[@class="functions docblock"]/li/a/@href').extract()
        for item in html_list6:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])
        
        html_list7 = response.xpath('//ul[@class="typedefs docblock"]/li/a/@href').extract()
        for item in html_list7:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])
        
        html_list8 = response.xpath('//ul[@class="constants docblock"]/li/a/@href').extract()
        for item in html_list8:
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        f = open('thirtyfour_sync/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('thirtyfour_sync/css/%s' % filename, 'w', encoding='utf-8')
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
                #if item.find('..', 0) == 0:
                #    item = self.root_url + item.split('/')[2]
                item = self.root_url + item
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

        f = open('thirtyfour_sync/%s' % filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1

