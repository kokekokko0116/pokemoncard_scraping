import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['yuyu-tei.jp']
    start_urls = ['http://yuyu-tei.jp/game_poc']

    # 以下本番用（すべてのシリーズを抽出）
    rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@data-class='buy']/li[@class='item_single_card']/ul/li[2]/ul/li/a"),callback="parse_item", follow=True),Rule(LinkExtractor(restrict_xpaths="//ul[@data-class='buy']/li[@class='item_single_card']/ul/li[3]/ul/li/a"),callback="parse_item", follow=True),)
    

    # 以下のコードはテスト用（最新弾のみ抽出）
    # rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@data-class='buy']/li[@class='item_single_card']/ul/li[2]/ul/li[1]/a"),callback="parse_item", follow=True),
    #          Rule(LinkExtractor(restrict_xpaths="//ul[@data-class='buy']/li[@class='item_single_card']/ul/li[3]/ul/li[7]/a"),callback="parse_item", follow=True),Rule(LinkExtractor(restrict_xpaths="//ul[@data-class='buy']/li[@class='item_single_card']/ul/li[3]/ul/li[10]/a"),callback="parse_item", follow=True),)
    

    
    def get_series_number(self,element):
        if element:
            return element.split(' ')[0].replace('[','').replace(']','')
        return element
    
    def get_series_name(self,element):
        if element:
            return ' '.join(element.split(' ')[1:]).strip()
        return element
    
    def get_number(self,element):
        if element:
            return element.lstrip().replace(' ','')
        return element
    
    def get_price(self,element):
        if element:
            return element.replace('円','')
        return element
    
    def get_rarerity(self,element):
        if element:
            return element.split(' ')[0]
        return element



    def parse_item(self, response):

        series = response.xpath("//div[@class='label_heading']/h2/text()").get()
        ancestor = response.xpath("//div[@class='card_list_box']//li[contains(@class,'card_unit')]")
            
        for x in ancestor:
            # カード名だけ一覧画面で取得
            name = x.xpath(".//p[@class='name']/a/text()").get()

            yield{
                'series_number':self.get_series_number(response.xpath("//div[@class='label_heading']/h2/text()").get()),
                'series_name':self.get_series_name(response.xpath("//div[@class='label_heading']/h2/text()").get()),
                'number':self.get_number(x.xpath(".//p[@class='id']/a/text()").get()),
                'name':name,
                'price':self.get_price(x.xpath(".//p[@class='price']/b/text()").get()),
                'rarerity':self.get_rarerity(x.xpath(".//p[@class='image']/img/@alt").get()),
            }
