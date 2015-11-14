# coding: utf-8


import requests,time
from bs4 import *
import os
import time

start = time.time()
'''叡叡沒有爬的 Htc-one_e8'''
#---------------基本參數修改資料會用到---------------
#手機廠牌的字典
MiDic = {1:"Mi_3",2:"MiRed_1s"}
HtcDic={1:"Desire601",2:"Desire310",3:"One_m8",4:"E8",5:"Desire610",7:"Butterfly2",8:"ButterflyS"}
SamsungDic = {1:"Note3_lte",2:"Core_Lite",3:"KZoom",4:"Core_lte",5:"S5",6:"Note3_Neo",7:"Grand_Neo",8:"Grand2",9:"J"}
SonyDic ={1:"M2",2:"T3",3:"Z1_lte",4:"Z2",5:"E1",6:"L",7:"Z1C"}
LgDic={1:"GPro2",2:"G3",3:"G2_mini",4:"GFlex"}
AsusDic = {1:"Zenfone6",2:"Zenfone5",3:"Zenfone4",4:"PadFoneS",5:"padfone_Infinity"}
#資料來源的字典
webDic ={1:"mobile01",2:"eprice",3:"PTT"}


'''---------------需要修改四個地方,以標記在下方---------------'''
Module =HtcDic[7]   #手機型號(用moduleDic裡面的值)
print Module
web = webDic[1]     #資料來源(用web裡面的值)
searchURL = "inurl%3Atopicdetail.php%3Ff%3D566%20%20butterfly2%20%E8%9D%B4%E8%9D%B62" #搜尋結果的url
file_dir ="G:/OneDrive/project/projectData/etl/" #存檔的最大路徑(程式會自己在本路徑下建立子資料夾)
'''--------------------------------------'''



#以下是連結的link(不要改)
format_link = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=zh_TW&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&start={0}&cx=partner-pub-2628371516912843:futcqntfmz3&q={1}&googlehost=www.google.com&callback=google.search.Search.apiary6299&nocache=1431498745670'
fileDirMerge = file_dir+"{0}{1}" #路徑變成format格式
saveDir = fileDirMerge.format(web+"/"+Module,"") #建立最大的資料夾(依資料來源+機型存)


#開每個機型的資料夾
if not os.path.isdir(fileDirMerge.format(web+"/"+Module,"")):
    os.makedirs(fileDirMerge.format(web+"/"+Module,""))
    print "openDir="+fileDirMerge.format(web+"/"+Module,"")
outtitle = open(fileDirMerge.format(web+"/"+Module,"/total"+Module+".txt"),'a') #總標題的檔

'''------------------開始爬蟲------------------'''
for k in range(9,11): #大頁數
    for i in range(1,11):   #每頁的1~10筆連結

        #開啟存content的檔案
        res = requests.get(format_link.format(str(int(k-1)*10),searchURL))#2.修改成自己的手機型號
        m = res.text.split(',\"unescapedUrl\":\"')[i]
        n = m.split('\",\"')[0]

        article_id = n.split('php?f=')[1].split('&t=') #切出手機跟文章id
        res_link = requests.get(n)
        soup = BeautifulSoup(res_link.text)

        '''標題'''
        if len(soup.select('.topic'))>0:
            outPut = open(fileDirMerge.format(web+"/"+Module+"/",Module+"_"+str(int(k-1)*10+int(i))+".txt"),'w')
            print fileDirMerge.format(web+"/"+Module+"/",Module+"_"+str(int(k-1))+str(int(i))+".txt")
            topic = soup.select('.topic')[0]
            print  str(int(k-1)*10+int(i))+"\t"+Module+'\t'+web.encode("utf-8")+'\t'+article_id[0].encode('utf-8')+'\t'+article_id[1].split('&')[0].encode('utf-8')+'\t'+n.encode('utf-8')+'\t'+topic.text.encode('utf-8')
            #把資料寫入content的檔案裡
            outPut.write('標題'+"\t"+topic.text.encode('utf-8')+'\n')

            #把資料寫入純標題的檔案裡
            outtitle.write(str(int(k-1)*10+int(i))+"\t"+Module+'\t'+web.encode("utf-8")+'\t'+article_id[0].encode('utf-8')+'\t'+article_id[1].split('&')[0].encode('utf-8')+'\t'+n.encode('utf-8')+'\t'+topic.text.encode('utf-8')+"\n")

            '''討論頁數'''
            page = soup.select('.numbers')[0]
            x = page.text.split(u'共')[1]
            y = int(x.split(u'頁')[0])

            for j in range(1,y+1):
                topic_link = n+'&p={}'.format(j) #n = m.split('\",\"')[0]  #換頁用
                #print"____________________________"
                #print topic_link
                res_topic = requests.get(topic_link).text
                soupContent = BeautifulSoup(res_topic)
                frames=soupContent.select(".single-post")
                for frame in frames:
                    if len(frame.select("blockquote"))>0:
                        for blockquote in frame.select("blockquote"):
                            blockquote.decompose()
                    authorId = frame.select('.fn a')[0]['id'].strip() #每篇文章中的每則評論的使用者id
                    authorName =  frame.select('.fn a')[0].text.strip()
                    dateOrg = frame.select('.date')[0].text.strip()
                    date = dateOrg.split(" ")[0].strip()
                    floor = dateOrg.split("#")[1].strip()
                    content = ''.join(frame.select('.single-post-content div')[0].text.strip().split())
                    outPut.write(web.encode("utf-8")+'\t'+article_id[1].split('&')[0].encode('utf-8')+"\t"+floor.encode("utf-8")+"\t"+authorId.encode("utf-8")+"\t"+authorName.encode("utf-8")+"\t"+date.encode("utf-8")+"\t"+content.encode("utf-8")+"\n")
                    #print web.encode("utf-8")+'\t'+article_id[1].encode('utf-8')+"\t"+floor.encode("utf-8")+"\t"+authorId.encode("utf-8")+"\t"+authorName.encode("utf-8")+"\t"+date.encode("utf-8")+"\t"+content.encode("utf-8")
                    #print "--------------------------"
                    time.sleep(0.2)

            outPut.close()
outtitle.close()
end = time.time()
print end-start




