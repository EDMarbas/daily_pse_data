import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
import re

from datetime import date


pattern_pc = r'\((.*?)%\)'

# Extract the numeric value inside parentheses and apply transformation
def process_percent_change(value):
    if not value or pd.isna(value):  # Check for empty string or None
        return None
    match = re.findall(pattern_pc, value)
    if match:
        try:
            percent_value = float(match[0])
            if 'down' in value:
                return -percent_value
            return percent_value
        except ValueError:
            return None  # In case conversion to float fails
    return None


pattern = r'-?\d*\.?\d+'

def clean_value(x):
    if isinstance(x, str):
        x = x.replace(',', '')
        match = re.findall(pattern, x)
        if match:
            return float(match[0])
    return 0



class PseSpider(scrapy.Spider):
    name = "pse"
    allowed_domains = ["edge.pse.com.ph", "localhost"]

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    values = [
        '643', '25', '196', '600', '683', '225', '213', '183', '184', '39',
        '624', '186', '223', '662', '648', '22', '668', '652', '680', '637',
        '601', '50', '189', '621', '703', '55', '19', '174', '176', '114',
        '15', '57', '48', '233', '121', '16', '212', '172', '612', '180',
        '686', '26', '701', '619', '14', '609', '177', '638', '52', '678',
        '178', '226', '649', '224', '602', '197', '220', '676', '80', '198',
        '193', '69', '610', '611', '221', '132', '94', '691', '657', '228',
        '693', '67', '651', '681', '642', '187', '31', '36', '68', '188',
        '671', '620', '33', '38', '679', '694', '34', '53', '56', '641',
        '673', '697', '108', '9', '260', '21', '62', '63', '66', '49', '633',
        '82', '674', '626', '690', '661', '613', '83', '660', '622', '201',
        '84', '203', '4', '85', '204', '134', '86', '210', '261', '639',
        '647', '70', '46', '71', '623', '190', '632', '653', '219', '191',
        '634', '81', '151', '689', '75', '181', '2', '88', '87', '672', '209',
        '236', '98', '227', '692', '234', '13', '60', '669', '136', '578',
        '629', '148', '97', '138', '107', '631', '664', '158', '96', '104',
        '139', '7', '608', '129', '150', '141', '699', '30', '214', '142',
        '478', '154', '112', '161', '237', '156', '688', '479', '654', '655',
        '222', '164', '147', '73', '163', '269', '630', '6', '8', '650',
        '644', '167', '168', '700', '124', '205', '37', '605', '698', '61',
        '115', '12', '119', '106', '145', '3', '175', '135', '1', '117',
        '128', '126', '687', '127', '118', '120', '144', '76', '137', '628',
        '232', '54', '684', '702', '153', '77', '195', '40', '635', '64',
        '646', '658', '157', '32', '143', '165', '160', '166', '65', '28',
        '607', '123', '695', '79', '122', '90', '665', '173', '656', '89',
        '263', '105', '192', '206', '102', '24', '677', '682', '663', '218',
        '78', '41', '599', '131', '685', '659', '100', '270', '627', '103',
        '625', '264', '606', '179', '704', '207', '43', '616', '45', '109',
        '20', '194', '640', '208', '705',
    ]


    def start_requests(self):
        # Iterate over the list of values and generate start URLs dynamically
        for value in self.values:
            # Construct the start URL with the value
            start_url = f"https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id={value}"

            # Yield a request for each start URL
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        finance_link = response.xpath("//ul[@class='companyTab']/li[4]/a/@href").get()

        yield response.follow(
                              finance_link, callback=self.parse_finance_page,
                              meta={
                                    'stock': response.xpath("//div[@id='contents']/form/select/option[1]/text()").get(),
                                    'last_price': response.xpath("//table[2]/tr[1]/td[1]/text()").get(),
                                    'value': response.xpath("//table[2]/tr[3]/td[1]/text()").get(),
                                    'volume': response.xpath("//table[2]/tr[4]/td[1]/text()").get(),
                                    'percent_change': response.xpath("//table[2]/tr[2]/td[1]/text()").get(),
                                    'week_high': response.xpath("//table[2]/tr[5]/td[1]/text()").get(),
                                    'week_low': response.xpath("//table[2]/tr[5]/td[2]/text()").get(),

                                    'open_price': response.xpath("//table[2]/tr[1]/td[2]/text()").get(),
                                    'high': response.xpath("//table[2]/tr[2]/td[2]/text()").get(),
                                    'low': response.xpath("//table[2]/tr[3]/td[2]/text()").get()

                              }
        )

    def parse_finance_page(self, response):
        stock = response.meta.get('stock')
        last_price = response.meta.get('last_price')
        value = response.meta.get('value')
        volume = response.meta.get('volume')
        percent_change = response.meta.get('percent_change')
        week_high = response.meta.get('week_high')
        week_low = response.meta.get('week_low')

        open_price = response.meta.get('open_price')
        high = response.meta.get('high')
        low = response.meta.get('low')

        book_value = response.xpath("//table[1]/tr[9]/td[1]/text()").get()
        earnings = response.xpath("//table[2]/tr[7]/td[1]/text()").get()
        dividend = response.xpath("//ul[@class='companyTab']/li[6]/a/@href").get()

        yield SplashRequest(
                            response.urljoin(dividend), self.parse_dividend_page, endpoint='execute',
                            args={'lua_source': self.script},
                            meta={
                                'stock': stock,
                                'last_price': last_price,
                                'value': value,
                                'volume': volume,
                                'percent_change': percent_change,
                                'book_value': book_value,
                                'earnings': earnings,
                                'week_high': week_high,
                                'week_low': week_low,

                                'open_price': open_price,
                                'high': high,
                                'low': low

                            }
        )

    def parse_dividend_page(self, response):
        stock = response.meta.get('stock')
        last_price = response.meta.get('last_price')
        value = response.meta.get('value')
        volume = response.meta.get('volume')
        percent_change = response.meta.get('percent_change')
        book_value = response.meta.get('book_value')
        earnings = response.meta.get('earnings')
        week_high = response.meta.get('week_high')
        week_low = response.meta.get('week_low')

        open_price = response.meta.get('open_price')
        high = response.meta.get('high')
        low = response.meta.get('low')

        last_dividend = response.xpath("//table/tbody/tr[1]/td[3]/text()").get()

        clean_percent_change = process_percent_change(percent_change)
        clean_book_values = clean_value(book_value)
        clean_earnings = clean_value(earnings)


        chart_date = date.today().strftime('%Y-%m-%d')

        yield {
            'stock': stock.strip() if stock else None,
            'last_price': last_price.replace(',', '').strip() if last_price else None,
            'value': value.replace(',', '').strip() if value else None,
            'volume': volume.replace(',', '').strip() if value else None,
            'percent_change': clean_percent_change,
            'eps': clean_earnings,
            'book_value': clean_book_values,
            'week_high': week_high.strip() if week_high else None,
            'week_low': week_low.strip() if week_low else None,
            'last_dividend': last_dividend.strip() if last_dividend else None,

            'open_price': open_price.replace(',', '').strip() if open_price else None,
            'high': high.replace(',', '').strip() if high else None,
            'low': low.replace(',', '').strip() if low else None,
            'chart_date': chart_date,
        }
    

    
