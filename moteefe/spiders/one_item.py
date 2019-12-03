import scrapy
import re
import json
from scrapy.loader import ItemLoader
from moteefe.items import MoteefeItem


class OneItemSpider(scrapy.Spider):
    name = 'mote_one'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def start_requests(self):
        url = "file:///home/baoha/moteefe/data_files/moteefe_item.html"
        yield scrapy.Request(
            url,
            headers=self.headers,
            callback=self.parse
        )
    
    def parse(self, response):
        products = []

        local_resources_json = re.findall("window.localeResources =(.+?);\n", response.body.decode("utf-8"), re.S)
        local_resources = json.loads(local_resources_json[0])

        product_names = local_resources.get('de').get('common').get('products').get('names')
        product_descriptions = local_resources.get('de').get('common').get('products').get('descriptions')

        product_list_json = json.loads(response.xpath("//script[@class='js-react-on-rails-component']/text()").get())

        product_list = product_list_json.get('state').get('page').get('products')

        campaign_products = product_list_json.get('state').get('page').get('campaign_products')
        campaign_mockups = product_list_json.get('state').get('page').get('campaign_mockups')

        for product_main in campaign_products:
            product_main_id = product_main.get('product_id')
            for product_references in product_list:
                if product_references.get('id') == product_main_id:
                    for color_id in product_main.get('color_ids'):
                        for color in product_references.get('colors'):
                            if color_id == color.get('id'):
                                for index, size in enumerate(product_references.get('sizes'), start=0):
                                    loader = ItemLoader(item=MoteefeItem())
                                    loader.add_value('Variant_Price', str(product_main.get('price')))
                                    loader.add_value('Variant_Compare_At_Price', str(product_main.get('pre_discounted_price')))
                                    loader.add_value('Handle', product_references.get('slug'))
                                    loader.add_value('Option_1_Name', "Color")
                                    loader.add_value('Option_1_Value', color.get('name'))
                                    loader.add_value('Option_2_Name', "Size")
                                    loader.add_value('Option_2_Value', size.get('name'))
                                    loader.add_value('Variant_SKU', product_references.get('slug')+"-"+color.get('name')+"-"+size.get('name'))
                                    for campaign_mockup in campaign_mockups:
                                        if campaign_mockup.get('color_id') == color_id and campaign_mockup.get('product_id') == product_main_id and campaign_mockup.get('image'):
                                            loader.add_value('Variant_Image', campaign_mockup.get('image').get('big'))
                                            break

                                    if index == 0:
                                    # Get Title
                                        name = product_references.get('name')
                                        aname = name.replace("common:products.names.", "")
                                        loader.add_value('Title', product_names.get(aname))
                                        # Get description
                                        details = product_references.get('details')
                                        adetails = details.replace("common:products.descriptions.", "")
                                        loader.add_value('Body_HTML', product_descriptions.get(adetails))
                                        # Get Type
                                        loader.add_value('Type', product_references.get('tracking_name'))
                                        loader.add_value('Tags', "")
                                        loader.add_value('Published', "TRUE")
                                    else:
                                        loader.add_value('Title', "")
                                        loader.add_value('Body_HTML', "")
                                        loader.add_value('Type', "")
                                        loader.add_value('Tags', "")
                                        loader.add_value('Published', "")

                                    products.append(loader.load_item())
                        
       
        for product in products:
            try:
                handle = product['Handle']
            except:
                handle = ""
            try:
                title = product['Title']
            except:
                title = ""
            try:
                Body_HTML = product['Body_HTML']
            except:
                Body_HTML = ""
            try:
                Type = product['Type']
            except:
                Type = ""
            try:
                Published = product['Published']
            except:
                Published = ""
            try:
                Published = product['Published']
            except:
                Published = ""
            try:
                Option_1_Name = product['Option_1_Name']
            except:
                Option_1_Name = ""
            try:
                Option_1_Value = product['Option_1_Value']
            except:
                Option_1_Value = ""
            try:
                Option_2_Name = product['Option_2_Name']
            except:
                Option_2_Name = ""
            try:
                Option_2_Value = product['Option_2_Value']
            except:
                Option_2_Value = ""
            try:
                Option_3_Name = product['Option_3_Name']
            except:
                Option_3_Name = ""
            try:
                Option_3_Value = product['Option_3_Value']
            except:
                Option_3_Value = ""
            try:
                Option_3_Value = product['Option_3_Value']
            except:
                Option_3_Value = ""
            try:
                Variant_SKU = product['Variant_SKU']
            except:
                Variant_SKU = ""
            try:
                Variant_Price = product['Variant_Price']
            except:
                Variant_Price = ""
            try:
                Variant_Compare_At_Price = product['Variant_Compare_At_Price']
            except:
                Variant_Compare_At_Price = ""
            try:
                Variant_Image = product['Variant_Image']
            except:
                Variant_Image = ""
            
            yield {
                'Handle':handle,
                'Title': title,
                'Body (HTML)':Body_HTML,
                'Vendor':"",
                'Type':Type,
                'Tags':"",
                'Published':Published,
                'Option1 Name':Option_1_Name,
                'Option1 Value':Option_1_Value,
                'Option2 Name':Option_2_Name,
                'Option2 Value':Option_2_Value,
                'Option3 Name':Option_3_Name,
                'Option3 Value':Option_3_Value,
                'Variant SKU':Variant_SKU,
                'Variant Grams':"",
                'Variant Inventory Tracker':"",
                'Variant Inventory Qty':"0",
                'Variant Inventory Policy':"continue",
                'Variant Fulfillment Service':"manual",
                'Variant Price':Variant_Price,
                'Variant Compare At Price':Variant_Compare_At_Price,
                'Variant Requires Shipping':"",
                'Variant Taxable':"",
                'Variant Barcode':"",
                'Image Src':"",
                'Image Position':"",
                'Image Alt Text':"",
                'Gift Card':"",
                'SEO Title':"",
                'SEO Description':"",
                'Google Shopping / Google Product Category':"",
                'Google Shopping / Gender':"",
                'Google Shopping / Age Group':"",
                'Google Shopping / MPN':"",
                'Google Shopping / AdWords Grouping':"",
                'Google Shopping / AdWords Labels':"",
                'Google Shopping / Condition':"",
                'Google Shopping / Custom Product':"",
                'Google Shopping / Custom Label 0':"",
                'Google Shopping / Custom Label 1':"",
                'Google Shopping / Custom Label 2':"",
                'Google Shopping / Custom Label 3':"",
                'Google Shopping / Custom Label 4':"",
                'Variant Image':Variant_Image,
                'Variant Weight Unit':"",
                'Variant Tax Code':"",
                'Cost per item':"",
            }