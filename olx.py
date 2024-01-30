import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from difflib import SequenceMatcher
from selenium import webdriver
import time
import datetime
import re


import scrapy
 

class OlxHouses(scrapy.Spider):
    name = 'olx'
 
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 5,  # Adicione um atraso de 1 segundo entre as solicitações
    }
 
    def start_requests(self):
        for page in range(1,100):
            yield scrapy.Request(f'https://www.olx.com.br/imoveis/venda/estado-rs/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/moinhos-de-vento?o={page}')
 
    def parse(self, response, **kwargs):
        html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        houses = html.get('props').get('pageProps').get('ads')
        for house in houses:
                    yield{
                            'title' : house.get('title'),
                            'price' : house.get('price'),
                            'location' : house.get('location'),
                            'propriedades': house.get('properties') 
                    }
            #pra rodar precisa dar um env na pasta do script e scrapy runspider
#PS D:\Imobiliaria> $env:PATH += ";C:\Users\igors\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"
