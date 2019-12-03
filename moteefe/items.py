# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoteefeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    Handle = scrapy.Field()
    Title = scrapy.Field()
    Image_Src = scrapy.Field()
    Image_Position = scrapy.Field()
    Image_Alt_Text = scrapy.Field()
    Body_HTML  = scrapy.Field()
    Type = scrapy.Field()
    Tags = scrapy.Field()
    Published = scrapy.Field()
    Option_1_Name = scrapy.Field()
    Option_1_Value = scrapy.Field()
    Option_2_Name = scrapy.Field()
    Option_2_Value = scrapy.Field()
    Option_3_Name = scrapy.Field()
    Option_3_Value = scrapy.Field()
    Variant_SKU = scrapy.Field()
    Variant_Price = scrapy.Field()
    Variant_Compare_At_Price = scrapy.Field()
    Variant_Image = scrapy.Field()
    Gift_Card = scrapy.Field()
    SEO_Title = scrapy.Field()
    SEO_Description = scrapy.Field()
    Google_Shopping_Gender = scrapy.Field()
    Google_Shopping_Age_Group = scrapy.Field()
    Cost_per_item = scrapy.Field()
    