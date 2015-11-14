
# coding: utf-8

# In[96]:

import requests;
import re;
from bs4 import BeautifulSoup;
link='https://www.ptt.cc/bbs/MobileComm/index{0}.html'
res=requests.get('https://www.ptt.cc/bbs/MobileComm/index.html',verify=False)
soup=BeautifulSoup(res.text)

lastpage = soup.select('.wide')[1]['href']
pagepattern = re.match(r'/bbs/MobileComm/index(\d+).html',lastpage )
pagenumber =  int(pagepattern.group(1))
#print pagenumber
for page in range(2516,int(pagenumber)+2):
    
    res1= requests.get(link.format(page),verify=False)
    soup1=BeautifulSoup(res1.text)
    title1=soup1.select('.title')
    
    #try:
    for bid_row in title1:                   #針對每一個在title1裡的bid_row
        links=[tag['href']for tag in bid_row.select('a')]  #且這個tag有針對bid_row去select
        if len(links)>0:
            link='https://www.ptt.cc'+links[0]
            pklinks=links[0].split('m/')[1]#pk links
            #print pklinks
            res2=requests.get(link,verify=False)
            soup2=BeautifulSoup(res2.text)
            #print soup2
            for con in soup2.select('.bbs-screen.bbs-content'):
                #print con
                #print "************************************"
                title=con.select('.article-meta-value')[2].text.split(']')[1]
                author=con.select('.article-meta-value')[0].text.split()[0]
                day=con.select('.article-meta-value')[3].text.split()[0]#星期
                month=con.select('.article-meta-value')[3].text.split()[1]#月份
                date1=con.select('.article-meta-value')[3].text.split()[2]#日期
                time=con.select('.article-meta-value')[3].text.split()[3]#時間
                year=con.select('.article-meta-value')[3].text.split()[4]#年分
                #a=('ptt'+'\t'+pklinks.encode('utf-8')+'\t'+link.encode('utf-8')+'\t'+title.encode('utf-8')+'\n')
                #print a

                mc = soup2.select('#main-content')[0]
                [i.decompose() for i in mc.select('span')]
                [i.decompose() for i in mc.select('div')]
                p= ''.join(mc.text.split('>')[0].script().split())#找出內文
                #print ('ptt'+'\t'+pklinks.encode('utf-8')+'\t'+link.encode('utf-8')+'\t'+title.encode('utf-8')+'\t'+p.encode('utf-8'))
                #print "--------------------------------------------------"
                for bid1 in con.select('.f2'):
                    print bid1
#                 for bid1 in con.select('.push'):
#                     print "for"
#                     author1=bid1.select('.push-userid')[0].text.split('>')[0]
#                     pushcontent=bid1.select('.push-content')[0].text.split(':')[1]
#                     time=bid1.select('.push-ipdatetime')[0].text
#                     contentoutput.write('ptt'+'\t'+author1.encode('utf-8')+'\t'+pushcontent.encode('utf-8')+'\t')
#                     print author1
                
