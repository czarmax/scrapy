import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from boursorama.items import TableItem

def filter_historic_data(s):
    if 'Données historiques' in s:
        return True

class TableRowLoader(ItemLoader):
    # called at add_xpath/css/value in spider
    # default_input_processor = MapCompose(str.strip)
    """ The result of the input processor is collected and kept in the Item Loader"""
    # called at load_item() in spider
    # default_output_processor = TakeFirst()
    elem_in = MapCompose(str.strip)
    #elem_out = Join()

"""
Both input and output processors must receive an iterator as their first argument. 
The output of those functions can be anything. 
The result of input processors will be appended to an internal list (in the Loader) 
containing the collected values (for that field). The result of the output processors 
is the value that will be finally assigned to the item.
"""


class BoursoSpider(scrapy.Spider):
    name = "LVMH"  # по этому названию spider будет запускаться
    allowed_domains = ["boursorama.com"]
    start_urls = [
        # список url'ов, которые будут использованы для начальных реквестов
        "https://www.boursorama.com/cours/1rPMCNV/"]

    def parse(self, response):
        loader = TableRowLoader(item=TableItem(), response=response)
        # важно чтобы string была названа как в items
        blocks = response.xpath('//div[@class="c-block "]').extract()
        for b in range(len(blocks)):
            if filter_historic_data(blocks[b]):
                for r in range(13):
                    # индексируем каждый row элемент с помощью %d
                    loader.add_xpath('elem', '//div[@class="c-block "][%d]'
                                             '//tr[%d]/text()' % (b, r))  # '//tr[@class="c-table__row"][%d]/td/text()' % i)
                    yield loader.load_item()

