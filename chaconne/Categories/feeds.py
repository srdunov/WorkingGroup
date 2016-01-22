#!/usr/bin/python3
# -*- coding: utf-8 -*-
import urllib.request as ulib
from lxml.html import fromstring
from lxml import etree
from collections import OrderedDict
import json
URL="http://www.chaconne.ru";

def GetBooksByPublish():
    num=0
    while(True):
        url = "http://www.chaconne.ru/catalog_izdat.php?cat=573&p="+str(num);
        html = ulib.urlopen(url).read().decode('cp1251','ignore');
        page = fromstring(html);
        path = ".//td[@class='pad7 pad8 pad4']/a";
        links = page.xpath(path);

        if(len(links)<1):
            break;
        for l in links:
            with open('feeds.json', 'a', encoding='utf8') as outfile:
                t=GetBooksInCat(l.attrib['href'],l.text);
                if(t):
                    json.dump(t, outfile, sort_keys = False, indent = 4, ensure_ascii = False);
                    outfile.write(",\n");
        num=num+1;
    return 1;

def GetBooksByAutors():    
    num=0
    while(True):
        url = "http://www.chaconne.ru/catalog_author.php?cat=573&p="+str(num);
        html = ulib.urlopen(url).read().decode('cp1251','ignore');
        page = fromstring(html);
        path = ".//td[@class='pad7 pad8 pad4']/a";
        links = page.xpath(path);

        if(len(links)<1):
            break;
        for l in links:
            with open('feeds.json', 'a', encoding='utf8') as outfile:
                t=GetBooksInCat(l.attrib['href'],l.text);
                if(t):
                    json.dump(t, outfile, sort_keys = False, indent = 4, ensure_ascii = False);
                    outfile.write(",\n");
        num=num+1;
    return 1;

def GetBooksInCat(link, name):
    result=OrderedDict();

    url=URL+'/'+link;
    
    result["url"]=url;
    result["list_name"]=name;

    html = ulib.urlopen(url).read().decode('cp1251','ignore');
    page = fromstring(html);
    path = ".//div[@class='small mar3']/b/text()";
    count = page.xpath(path);

    min_price = 0
    max_price = 0
    num=0;
    num_page=1;
    item_list=[]

    if(len(count)>0):
        result["list_count"]=int(count[0].replace('Всего: ',''));
    else:
        return False;
    
    while(num<30):
        html = ulib.urlopen(url+'&p='+str(num_page)).read().decode('cp1251','ignore');
        page = fromstring(html);
        path = ".//h4[@class='media-heading']/a";
        links = page.xpath(path);
        
        if(len(links)<1):
            break;
            #return OrderedDict();
        for l in links:
            try:
                books, price = GetData(l.attrib['href'],l.text)
                if(price!=0):
                    if(min_price==0 or price<min_price):
                        min_price=price
                    if(max_price==0 or price>max_price):
                        max_price=price
                    item_list.append(books);
                else:
                   num = num-1; 
            except Exception:
                num = num-1;
            num = num+1;
            if(num==30):
                break;
        num_page=num_page+1;

    if (num<1):
        return False;
       
    result["item_list"]=item_list;
    result["item_price_min"]=OrderedDict([('currency', 'RUR'), ('type', 'currency'), ('content', min_price)]);
    result["item_price_max"]=OrderedDict([('currency', 'RUR'), ('type', 'currency'), ('content', max_price)]);
    return result;

def GetData(link,name):
    result=OrderedDict();
    result["url"]=URL+link;
    result["name"]=name;

    
    url = URL+link;
    html = ulib.urlopen(url).read().decode('cp1251','ignore');
    page = fromstring(html);
    path = ".//table[@class='table table-striped autowidth']/tr/td[1]/descendant-or-self::*[not(text()='')]/text()";
    idents = page.xpath(path);
    path = ".//table[@class='table table-striped autowidth']/tr/td[2]/descendant-or-self::*[not(text()='')]/text()";
    vals = page.xpath(path)
    good = dict(zip(idents, vals))

    path = ".//div[@class='rel ']/img[@class='cover']/@src";
    im = page.xpath(path)
    if(len(im)>0):
        result["images"]=[im[0]];
    
    if("автор:" in good):
        result["author"]=good["автор:"];
        
    path = ".//div[@id='price-detail']/*/span[@class='price']/span/text()";
    price = page.xpath(path)
    p_out=0
    if(len(price)>0):
        p=''.join(x for x in price[0] if x.isdigit())
        p_out=int(p)
        result["price"] = OrderedDict([('currency', 'RUR'), ('type', 'currency'), ('content', p_out)])
        #result["price"]={"currency": "RUR", "type": "currency", "content": price[0]};

    return result,p_out;

f = open('feeds.json', 'w');
f.close();
GetBooksByPublish();
GetBooksByAutors();
