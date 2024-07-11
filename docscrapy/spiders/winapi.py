import scrapy
import os

class RustSpider(scrapy.Spider):
    name = 'winapi'
    allowed_domains = ['docs.rs']
    start_urls = ['https://docs.rs/winapi/latest/winapi/all.html']
    root_url = 'https://docs.rs'
    std_url = 'https://docs.rs/winapi/latest/winapi/'
    inner_href = []
    css_index_list = []
    sub_index = 0
    css_i = 0
    count = 0


    def parse(self, response):
        print('main start...')
        if not os.path.exists('winapi/css'):
            os.makedirs('winapi/css')
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        print('css:')
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if css not in self.inner_href:
                txt = item
                #if item.find('..', 0) == 0:
                #    item = self.root_url + item.split('/')[1]
                item = self.root_url + item
                print(item)
                yield scrapy.Request(item, self.css_parse)
                i = len(self.css_index_list)
                self.css_index_list.append(i)
                html = html.replace(txt, 'css/%s' % css)
                self.inner_href.append(css)
            else:
                html = html.replace(item, 'css/%s' % css)

        html_list = response.xpath('//section[@class="content"]/ul/li/a/@href').extract()
        i = 0
        for item in html_list:
            print('%d:%s' % (i, item))
            i += 1
            self.count += 1
            yield scrapy.Request('%s%s' % (self.std_url, item), self.sub_parse)
            html = html.replace(item, item.split('/')[-1])

        script_list = response.xpath('//script').extract()
        for item in script_list:
            html = html.replace(item, '')
        
        img_list = response.xpath('//img').extract()
        for item in img_list:
            html = html.replace(item, '')

        f = open('winapi/index.html', 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('main end...')
    
    def css_parse(self, response):
        print('css_parse start...')
        file_arr = response.url.split('/')
        filename = file_arr[len(file_arr) - 1]
        f = open('winapi/css/%s' % filename, 'w', encoding='utf-8')
        f.write(response.text)
        f.flush()
        f.close()
        self.css_i += 1
        print('css_parse end...')
    
    def sub_parse(self, response):
        print('sub%d/%d start...' % (self.sub_index, self.count))
        html = response.text
        css_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
        for item in css_list:
            item = item.split('?')[0]
            css_array = item.split('/')
            css = css_array[len(css_array) - 1]
            if item not in self.inner_href:
                txt = item
                # if item.find('..', 0) == 0:
                    # item = self.root_url + item.split('/')[2]
                print('%s%s' % (self.root_url, item))
                yield scrapy.Request('%s%s' % (self.root_url, item), self.css_parse)
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

        filename = response.url.split('/')[-1]
        print('filename:', filename)

        f = open('winapi/%s' % filename, 'w', encoding='utf-8')
        f.write(html)
        f.flush()
        f.close()
        print('sub%d end...' % self.sub_index)
        self.sub_index += 1

