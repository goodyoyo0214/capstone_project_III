# coding=utf-8
__author__ = 'BigData'
import requests
from bs4 import *
import io

html = requests.get("http://www.eprice.com.tw/mobile/buyerguide/?manu=Samsung&class=1")
html.encoding= "utf-8"
module = open("E:/project/projectData/dic/module/moduleSam.txt","w")
soup =BeautifulSoup(html.text)
#print soup.select(".prod-list")[0]
#soup.select("div.other-prod-list")[0].decompose()
#print soup
#print soup

moduleN = soup.select("a.img")


count = 1 #htc用的

for i in moduleN:
    #print  i['title']


    #SAMSUNG切字
    if len(i['title'].split("Galaxy"))>1 and count<51:
        print count,i['title']
        count +=1
        fullName = ''.join(i['title'].split("Samsung")[1].encode("utf-8").split())
        lessName = ''.join(i['title'].split("Galaxy")[1].encode("utf-8").split())
        fullNameU = fullName.upper()
        lessNameU = lessName.upper()
        fullNameD = fullName.lower()
        lessNameD = lessName.lower()
        brandAName = "Samsung"+''.join(i['title'].split("Galaxy")[1].encode("utf-8").split())
        brandANameU = brandAName.upper()
        brandANameD = brandAName.lower()
        print fullName+"\t"+lessName+"\t"+fullNameU+"\t"+lessNameU+"\t"+fullNameD+"\t"+lessNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
        module.write(fullName+"\n"+lessName+"\n"+fullNameU+"\n"+lessNameU+"\n"+fullNameD+"\n"+lessNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")
    '''
    #lg切字
    print i['title']
    fullName = ''.join(i['title'].split("LG")[1].encode("utf-8").split())
    fullNameU = fullName.upper()
    fullNameD = fullName.lower()
    brandAName=''.join(i['title'].encode("utf-8").split())
    brandANameU = brandAName.upper()
    brandANameD = brandAName.lower()
    brandANameN = "Lg"+''.join(i['title'].split("LG")[1].encode("utf-8").split())
    brandANameNU = brandANameN.upper()
    brandANameND = brandANameN.lower()
    print fullName+"\t"+fullNameU+"\t"+fullNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD+"\t"+brandANameN+"\t"+brandANameNU+"\t"+brandANameND
    module.write(fullName+"\n"+fullNameU+"\n"+fullNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n"+brandANameN+"\n"+brandANameNU+"\n"+brandANameND+"\n")
    '''
    '''
    #htc切字
    if count <78:
        print  i['title']

        fullName = ''.join(i['title'].split("HTC")[1].encode("utf-8").split())
        fullNameU = fullName.upper()
        fullNameD = fullName.lower()
        brandAName=''.join(i['title'].encode("utf-8").split())
        brandANameU = brandAName.upper()
        brandANameD = brandAName.lower()
        print fullName+"\t"+fullNameU+"\t"+fullNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
        module.write(fullName+"\n"+fullNameU+"\n"+fullNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")

        count +=1

    '''
    '''
    #acer切字
    if len(i.text.split("Liquid"))>1:
        fullName = ''.join(i.text.split("Acer")[1].encode("utf-8").split())
        lessName = ''.join(i.text.split("Liquid")[1].encode("utf-8").split())
        fullNameU = fullName.upper()
        lessNameU = lessName.upper()
        fullNameD = fullName.lower()
        lessNameD = lessName.lower()
        brandAName = "Acer"+''.join(i.text.split("Liquid")[1].encode("utf-8").split())
        brandANameU = brandAName.upper()
        brandANameD = brandAName.lower()
        print fullName+"\t"+lessName+"\t"+fullNameU+"\t"+lessNameU+"\t"+fullNameD+"\t"+lessNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
        module.write(fullName+"\n"+lessName+"\n"+fullNameU+"\n"+lessNameU+"\n"+fullNameD+"\n"+lessNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")
    '''
    '''
    #sony切字
    fullName = ''.join(i['title'].split("SONY")[1].encode("utf-8").split())
    lessName = ''.join(i['title'].split("Xperia")[1].encode("utf-8").split())
    fullNameU = fullName.upper()
    lessNameU = lessName.upper()
    fullNameD = fullName.lower()
    lessNameD = lessName.lower()
    brandAName = "Sony"+''.join(i['title'].split("Xperia")[1].encode("utf-8").split())
    brandANameU = brandAName.upper()
    brandANameD = brandAName.lower()
    print fullName+"\t"+lessName+"\t"+fullNameU+"\t"+lessNameU+"\t"+fullNameD+"\t"+lessNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
    module.write(fullName+"\n"+lessName+"\n"+fullNameU+"\n"+lessNameU+"\n"+fullNameD+"\n"+lessNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")
    '''
    '''
    #asus切字
    if len(i['title'].split("Fone")) > 1:
        print i.text
        fullName = ''.join(i['title'].split("ASUS")[1].encode("utf-8").split())
        fullNameU = fullName.upper()
        fullNameD = fullName.lower()
        brandAName="Asus"+''.join(i['title'].split("ASUS")[1].encode("utf-8").split())
        brandANameU = brandAName.upper()
        brandANameD = brandAName.lower()
        print fullName+"\t"+fullNameU+"\t"+fullNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
        module.write(fullName+"\n"+fullNameU+"\n"+fullNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")
    if len(i['title'].split("fone")) > 1:
        print i.text
        fullName = ''.join(i['title'].split("ASUS")[1].encode("utf-8").split())
        fullNameU = fullName.upper()
        fullNameD = fullName.lower()
        brandAName="Asus"+''.join(i['title'].split("ASUS")[1].encode("utf-8").split())
        brandANameU = brandAName.upper()
        brandANameD = brandAName.lower()
        print fullName+"\t"+fullNameU+"\t"+fullNameD+"\t"+brandAName+"\t"+brandANameU+"\t"+brandANameD
        module.write(fullName+"\n"+fullNameU+"\n"+fullNameD+"\n"+brandAName+"\n"+brandANameU+"\n"+brandANameD+"\n")
    '''
module.close()