# -*- coding: utf-8 -*-
import urllib
from lxml.html import fromstring
from lxml import etree
import re
import datetime
import codecs
import json

def FormatPhone(num):
    t=""
    arr=num.split(', ')
    for i in xrange(len(arr)):
        number = arr[i].replace(' ','')
        if(number[0]=="7"):
            t+=("+"+number[0]+" ("+number[1:4]+") "+number[4:7]+"-"+number[7:9]+"-"+number[9:])
        elif(number[0]=="8"):
            t+=(number[0]+" ("+number[1:4]+") "+number[4:7]+"-"+number[7:9]+"-"+number[9:])
        else:
            t+=("+7"+" ("+number[0:4]+") "+number[4:7]+"-"+number[7:9]+"-"+number[9:])
        if(len(arr)>1 and i<len(arr)-1):
            t+=", "
    return t

def GetFeeds():    
    url = "http://kari.com/by/shops"

    html = urllib.urlopen(url).read().decode('utf-8','ignore')
    list_cont = re.search('storesMapInstance.setData\(\{stores\: \[(.*?)\]',html)
    html = list_cont.group(1)
    mathes = re.findall('{.*?}',html)

    xml = etree.Element('companies', nsmap={'xi':"http://www.w3.org/2001/XInclude"}, version="2.1");
    
    for i in mathes:
        json_dict = json.loads(i)
        
        company = etree.Element("company");
        etree.SubElement(company, "company-id").text = str(json_dict["ID"]);
        if("PROPERTY_COMPANY" in json_dict):
            lang = json_dict["PROPERTY_COMPANY"]
        else:
            lang="ru"
            
        if("NAME" in json_dict):
            name = etree.SubElement(company, "name")
            name.text = json_dict["NAME"];
            name.set("lang",lang)
        
        if(lang=="ua"):
            country = u"Украина"
        elif(lang=="by"):
            country = u"Белоруссия"
        elif(lang=="kz"):
            country = u"Казахстан"
        else:
            country = u"Россия"
        con=etree.SubElement(company, "country")
        con.text = country
        con.set("lang",lang)
        
        
        if("PROPERTY_ADDRESS" in json_dict):
            key = json_dict["PROPERTY_ADDRESS"].replace('\n','')
            adress = etree.SubElement(company, "address")
            adress.text = json_dict["PROPERTY_ADDRESS"];
            adress.set("lang",lang)
        if("PROPERTY_KIDS_ASSORTMENT" in json_dict):
            if(json_dict["PROPERTY_KIDS_ASSORTMENT"]=="1"):
                etree.SubElement(company, "rubric-id").text = "36609242320";
                etree.SubElement(company, "rubric-id").text = "184107248";
            else:
                etree.SubElement(company, "rubric-id").text = "184107941";
                etree.SubElement(company, "rubric-id").text = "184107943";
                etree.SubElement(company, "rubric-id").text = "184107935";
        else:
            etree.SubElement(company, "rubric-id").text = "184107941";
            etree.SubElement(company, "rubric-id").text = "184107943";
            etree.SubElement(company, "rubric-id").text = "184107935";
        
        etree.SubElement(company, "url").text = url+"/"+str(json_dict["ID"]);
        etree.SubElement(company, "actualization-date").text = datetime.datetime.now().strftime('%d.%m.%Y')

        if("PROPERTY_LAT" in json_dict and "PROPERTY_LON" in json_dict):
            coord = etree.SubElement(company, "coordinates")
            etree.SubElement(coord, "lon").text = json_dict["PROPERTY_LON"]
            etree.SubElement(coord, "lat").text = json_dict["PROPERTY_LAT"]

        if("PROPERTY_MANAGER_PHONE" in json_dict):
            phone = etree.SubElement(company, "phone")
            etree.SubElement(phone, "ext")
            etree.SubElement(phone, "type").text = "phone"
            etree.SubElement(phone, "number").text = FormatPhone(json_dict["PROPERTY_MANAGER_PHONE"])
            etree.SubElement(phone, "info").text = u"менеджер"

        if("PROPERTY_WORKTIME" in json_dict):
            work = etree.SubElement(company, "working-time")
            work.set("lang",lang)
            work.text =  json_dict["PROPERTY_WORKTIME"]
        #html = urllib.urlopen(url+"/"+str(json_dict["ID"])).read().decode('utf-8','ignore')
        #path=".//a[@class='header_phone_val']/text()"
        #page = fromstring(html)
        #sub_num=page.xpath(path)
        
        #if(len(sub_num)>0):
            #phone = etree.SubElement(company, "phone")
            #etree.SubElement(phone, "ext")
            #etree.SubElement(phone, "type").text = "phone"
            #etree.SubElement(phone, "number").text = FormatPhone(sub_num[0])
            #etree.SubElement(phone, "info").text = u"общий"
            #print(FormatPhone(sub_num[0]))
        xml.append(company)
        
            
    s=etree.tounicode(xml, pretty_print=True)
    with codecs.open('companies.xml', 'w','utf-8') as outfile:
        outfile.write("<?xml version='1.0' encoding='utf-8'?>\n")
        outfile.write(s);

GetFeeds();

        
