#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib.request as ulib
from lxml.html import fromstring
from lxml import etree
from collections import OrderedDict
import json
URL="http://www.chaconne.ru";

def GetBooks():
    f = open('data.json', 'w');
    f.close();

    num_page=0;
    num=0
    #while(num<30001):
    while(True):
        url = "http://www.chaconne.ru/catalog_name.php?cat=573&p="+str(num_page);
        html = ulib.urlopen(url).read().decode('cp1251','ignore');
        page = fromstring(html);
        path = ".//h4[@class='media-heading']/a";
        links = page.xpath(path);
        
        if(len(links)<1):
            break;
        for l in links:
            with open('data.json', 'a', encoding='utf8') as outfile:
                try:
                    json.dump(GetData(l.attrib['href'],l.text), outfile, sort_keys = False, indent = 4, ensure_ascii = False);
                    outfile.write(",\n");
                except Exception:
                    num = num-1;            
        num=num+20;
        num_page=num_page+1;
        print('Обработано книг:',num)
    return 1;

def GetData(link,name):
    result=OrderedDict();
    result["url"]=URL+link;
    result["name"]=name;

    
    url = URL+link;
    html = ulib.urlopen(url).read().decode('cp1251','ignore');
    page = fromstring(html);
    path = ".//table[@class='table table-striped autowidth']/tr/td[1]/*/text()";
    idents = page.xpath(path);
    path = ".//table[@class='table table-striped autowidth']/tr/td[2]";
    vals = page.xpath(path)
    vals_n=[]
    for v in vals:
        vals_n.append(v.text_content())
    good = dict(zip(idents, vals_n))

    path = ".//div[@class='rel ']/img[@class='cover']/@src";
    im = page.xpath(path)
    if(len(im)>0):
        result["images"]=[im[0]];
    
    if("автор:" in good):
        result["author"]=good["автор:"];
        
    if("издательство:" in good):
        result["publisher"]=good["издательство:"];

    path = ".//div[@class='small mar2 just']/text()";
    desc = page.xpath(path)
    if(len(desc)>0):
        result["description"]=''.join(desc);
        
    path = ".//div[@id='price-detail']/*/span[@class='price']/span/text()";
    price = page.xpath(path)
    if(len(price)>0):
        result["price"] = OrderedDict([('currency', 'RUR'), ('type', 'currency'), ('content', int(price[0].replace(' ','')))])
        #result["price"]={"currency": "RUR", "type": "currency", "content": price[0]};
        
    if("интернет магазин:" in good):
        result["availability"]=good["интернет магазин:"];
        
    if("год выпуска:" in good):
        try:
            result["year"]=int(good["год выпуска:"]);
        except Exception:
            if "year" in result: del result['year']
        
    if("оформление:" in good):
        result["cover"]=good["оформление:"];
        
    if("страниц:" in good):
        try:
            result["pages"]=int(good["страниц:"]);
        except Exception:
            if "pages" in result: del result['pages']
        
    if("ISBN:" in good):
        result["isbn"]=good["ISBN:"];

    return result;
GetBooks();

        
