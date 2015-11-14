
# coding: utf-8

# In[11]:

# -*- coding: <encoding name>-*-

import requests,time,re
from bs4 import BeautifulSoup
format_link = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=zh_TW&prettyPrint=false&source=gcsc&gss=.tw&sig=23952f7483f1bca4119a89c020d13def&start={0}&cx=partner-pub-2614970773838551:94vq76eazbo&q={1}&googlehost=www.google.com.tw&callback=google.search.Search.apiary78&nocache=1430127546425'
outTitle = open('eprice/mi3/totaltopic.txt','w')# 另存的標題檔,改為自己的存放方式

for k in range(1,11):
    #print "----------------------------------------------------------------"
    for i in range(1,11):
        outPut = open('eprice/mi3/{}.txt'.format(str(int(k-1)*10+int(i))),'w')#1.修改此處的目錄,改為自己的存放方式
        res = requests.get(format_link.format(str(int(k-1)*10),'%22%E7%B4%85%E7%B1%B31S%22%20%7C%20%22%E7%B4%85%E7%B1%B31s%22'))#2.修改成自己的手機型號
                                                                # Network 裡 Script 中 &q= 與 &googlehost 之間的東西
        #res.encoding='utf-8'
        #print  res.text
        m = res.text.split(',\"unescapedUrl\":\"')[i] #切出每篇 url
        n = m.split('\",\"')[0] # n=每篇文章的url (unicode)
        #print n
        #print len(n.split("intro"))
       
        if len(n.split("/talk/"))>1: #去掉第一篇介紹文 避免他抓不到而error
            
            article_id = n.split('/talk/')[1].split('/1/')[0].split('/') 
            #print article_id[0]+'\t'+article_id[1]
            #以上為手機的分類ID與文章的ID
            #print page_url
            res_link = requests.get(n)
            res_link.encoding='utf-8'
            #print 'page'+page

            fsoup = BeautifulSoup(res_link.text) #為了找出 MaxPage

            if len(fsoup.select('.title'))>0: #內文裡的標題文字
                topic = fsoup.select('.title')[0]
                #topic.encoding = 'utf-8'
                #print topic.text
                outPut.write('TITLE'+'\t'+topic.text.encode("UTF-8")+'\n')
                outTitle.write(format(str(int(k-1)*10+int(i)))+'\t'+article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+n.encode('utf-8')+'\t'+topic.text.encode('utf-8')+'\n')
                #以上為寫入標題
                #outTitle.write(n) #url寫入 TXT

                artical_url = n.split('/1/')[0] #切出頁數之前的url

                if len(fsoup.select('.pagelink a'))>0: 
                    maxpage = fsoup.select('.pagelink')[0].findAll('a')[-2].text.encode('utf-8')
                    if len(maxpage.split("..."))>1:
                        maxpage = int(maxpage.split('...')[1]) #頁數超出10頁
                    #找出最大頁數
                else:
                    maxpage = str(1) #若只有一頁 maxpage給1
                #print maxpage    
                
                    #最大頁數
                    #print maxpage
                    #print artical_url
                for page in range(1,int(maxpage)+1):

                    page_url = artical_url.encode('utf-8')+'/'+str(page)+'/'
                    #print page_url
                    content_link = requests.get(page_url)
                    content_link.encoding = 'utf-8'

                    soup = BeautifulSoup(content_link.text)
                    #print soup.text

                    contents = soup.findAll("dd",{"class":"enabled"})
                    #print contents
                    #print "_____________________________________________________"
                    for content in contents: #每一樓
                        #print content
                        #print content.text
                       
                        name = content.findAll('a',{"class":"nickname"})[0] #暱稱
                        nickname = name.text
                        nameid = str(name['href']).split('?u=')[1] #id
                        #print nicknameid
                        #暱稱 id
                        floor = content.findAll('em',{"class":"floor"})[0].text
                        #print floor
                        #幾樓
                        date = content.findAll('em',{"class":"date"})[0].text.encode('utf-8').split('發表於 ')[1]
                        #print date
                        #發表日期
                        
                        if len(content.select('.quote'))>0:
                            #print "if"
                            quoteto = content.select('.comment')[0].select('.quote')[0].decompose()
                            quoteto_split = content.select('.comment')[0].text
                            commentSplite = ''.join(quoteto_split.split())
                            print article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+floor.encode('utf-8')+'\t'+date.encode('utf-8')+'\t'+nameid.encode('utf-8')+'\t'+nickname.encode('utf-8')+'\t'+commentSplite.encode('utf-8')+'\n'
                            
                            #print quoteto_split.text
                        #去掉引用
                            #outPut.write(article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+floor.encode('utf-8')+'\t'+date.encode('utf-8')+'\t'+nameid.encode('utf-8')+'\t'+nickname.encode('utf-8')+'\t'+quoteto_split.encode('utf-8')+'\n')
                        else:
                            #print "else"
                            word = content.select('.user-comment-block')[0].select('.comment')[0].text #每一篇的第一則留言
                            comment = ''.join(word.split()) #融合成一行
                            print article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+floor.encode('utf-8')+'\t'+date.encode('utf-8')+'\t'+nameid.encode('utf-8')+'\t'+nickname.encode('utf-8')+'\t'+comment.encode('utf-8')+'\n'
        
                        #內文
                        #outPut.write(article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+floor.encode('utf-8')+'\t'+date.encode('utf-8')+'\t'+nameid.encode('utf-8')+'\t'+nickname.encode('utf-8')+'\t'+comment.encode('utf-8')+'\n')
                        
                        #fb_comment = soup.select('.fb-comment-block')[0]
                        #fb_nickname = fb_comment.select('.profilename')
                        #fb_posttext = fb_comment.select('postText')
                        #print fb_comment#+'\t'+fb_nickname+'\t'+fb_posttext
                        #print fb_nickname
                        #fb留言

                        #print type(floor),type(nameid),type(nickname),type(comment)
                        time.sleep(0.1)
                        # print quoteto
                        #print content[0].text

                        #rint content[1].text

                        #print ''.join(content.split())
                        #outPut.write(content.text.encode('utf-8')+'\n')

    outPut.close()
outTitle.close()


# In[ ]:




# In[4]:

outPut.close()
outTitle.close()


# #規格
# 

# In[42]:

# -*- coding: <encoding name>-*-

import requests,time,re
from bs4 import BeautifulSoup
format_link = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=zh_TW&prettyPrint=false&source=gcsc&gss=.tw&sig=23952f7483f1bca4119a89c020d13def&start={0}&cx=partner-pub-2614970773838551:94vq76eazbo&q={1}&googlehost=www.google.com.tw&callback=google.search.Search.apiary78&nocache=1430127546425'
outTitle = open('eprice/mi1s/totaltopic.txt','w')# 另存的標題檔,改為自己的存放方式

for k in range(1,11):
    #print "----------------------------------------------------------------"
    for i in range(1,11):
        outPut = open('eprice/mi1s/{}.txt'.format(str(int(k-1)*10+int(i))),'w')#1.修改此處的目錄,改為自己的存放方式
        res = requests.get(format_link.format(str(int(k-1)*10),'%22%E7%B4%85%E7%B1%B31S%22%20%7C%20%22%E7%B4%85%E7%B1%B31s%22'))#2.修改成自己的手機型號
                                                                # Network 裡 Script 中 &q= 與 &googlehost 之間的東西
        #res.encoding='utf-8'
        #print  res.text
        m = res.text.split(',\"unescapedUrl\":\"')[i] #切出每篇 url
        n = m.split('\",\"')[0] # n=每篇文章的url (unicode)
        #print n
        #print len(n.split("intro"))
        if len(n.split("intro"))>1:
            
            intro_link = requests.get(n)
            intro_link.encoding='utf-8'
            intro_article = BeautifulSoup(intro_link.text)
            table = intro_article.findAll('ul',{'class':'featurelist'})[0]
            #for i in range(1,len())
            table_white = table.select('li')
            for each_table in table_white:
                #print each_table
                #print "--------------------------------"
                whiteleft = each_table.select('label')[0].text
                whiteright = each_table.select('div')[0].text
            
                #gray = table.findAll("li",{'class':"gray"})
                print whiteleft
                print"______________________________________________"
                print whiteright


# #測試DECOMPOSE()

# In[3]:

import requests,time,re
from bs4 import BeautifulSoup
format_link = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=zh_TW&prettyPrint=false&source=gcsc&gss=.tw&sig=23952f7483f1bca4119a89c020d13def&start={0}&cx=partner-pub-2614970773838551:94vq76eazbo&q={1}&googlehost=www.google.com.tw&callback=google.search.Search.apiary78&nocache=1430127546425'
outTitle = open('eprice/mi3/totaltopic.txt','w')# 另存的標題檔,改為自己的存放方式

for k in range(1,11):
    #print "----------------------------------------------------------------"
    for i in range(1,11):
        outPut = open('eprice/mi3/{}.txt'.format(str(int(k-1)*10+int(i))),'w')#1.修改此處的目錄,改為自己的存放方式
        res = requests.get(format_link.format(str(int(k-1)*10),'%22%E5%B0%8F%E7%B1%B33%22%7C%22%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%A9%9F3%22%7C%22%E7%B1%B33%22'))#2.修改成自己的手機型號
                                                                # Network 裡 Script 中 &q= 與 &googlehost 之間的東西
        #res.encoding='utf-8'
        #print  res.text
        m = res.text.split(',\"unescapedUrl\":\"')[i] #切出每篇 url
        n = m.split('\",\"')[0] # n=每篇文章的url (unicode)
        #print n
        #print len(n.split("intro"))
       
        if len(n.split("/talk/"))>1: #去掉第一篇介紹文 避免他抓不到而error
            
            #if len(n.split('market'))==1:
                #print "market " , n
                #if len(n.split('buyerguide'))==1:
                    #print "buyerguide " , n
                    #if len(n.split("compare"))==1:
                        #if len(n.split('/0/'))==1:
                            #if len(n.split('pk'))==1:
                                #print n
            
            article_id = n.split('/talk/')[1].split('/1/')[0].split('/') 
            #print article_id[0]+'\t'+article_id[1]
            #以上為手機的分類ID與文章的ID
            #print page_url
            res_link = requests.get(n)
            res_link.encoding='utf-8'
            #print 'page'+page

            fsoup = BeautifulSoup(res_link.text) #為了找出 MaxPage

            if len(fsoup.select('.title'))>0: #內文裡的標題文字
                topic = fsoup.select('.title')[0]
                #topic.encoding = 'utf-8'
                #print topic.text
                outPut.write('TITLE'+'\t'+topic.text.encode("UTF-8")+'\n')
                outTitle.write(format(str(int(k-1)*10+int(i)))+'\t'+article_id[0].encode('utf-8')+'\t'+article_id[1].encode('utf-8')+'\t'+n.encode('utf-8')+'\t'+topic.text.encode('utf-8')+'\n')
                #以上為寫入標題
                #outTitle.write(n) #url寫入 TXT

                artical_url = n.split('/1/')[0] #切出頁數之前的url

                if len(fsoup.select('.pagelink a'))>0: 
                    maxpage = fsoup.select('.pagelink')[0].findAll('a')[-2].text.encode('utf-8')
                    if len(maxpage.split("..."))>1:
                        maxpage = int(maxpage.split('...')[1]) #頁數超出10頁
                    #找出最大頁數
                else:
                    maxpage = str(1) #若只有一頁 maxpage給1
                #print maxpage    
                
                    #最大頁數
                    #print maxpage
                    #print artical_url
                for page in range(1,int(maxpage)+1):

                    page_url = artical_url.encode('utf-8')+'/'+str(page)+'/'
                    #print page_url
                    content_link = requests.get(page_url)
                    content_link.encoding = 'utf-8'

                    soup = BeautifulSoup(content_link.text)
                    #print soup.text

                    #floormax = soup.findAll('em',{"class":"floor"})[-1].text.encode("utf-8").split('樓')[0]
                    #print floormax 
                    #每頁最大樓數 PS用不到

                    contents = soup.findAll("dd",{"class":"enabled"})
                    #print contents
                    print "_____________________________________________________"
                    for content in contents: #每一樓
                        #print content
                        #print content.text
                        if len(content.select('.quote'))>0:
                            #quotetoOrigen = content.select('.comment')[0]
                            print quotetoOrigen
                            quoteto = content.select('.quote')[0].decompose()
                            print "----------------------"
                            quoteto_split = content.select('.comment')[0]
                            print quoteto_split
                            print "*****************************************"
                            
                            time.sleep(0.1)
                            


# In[ ]:



