# encoding=utf-8
# reload(sys)
import codecs

import MySQLdb, io
import glob


BOM = codecs.BOM_UTF8.decode('utf8') #處理編碼的問題

#cnx = MySQLdb.connect("localhost","dbID","dbpasswd","dbname")

cnx = MySQLdb.connect(host="10.120.28.14", user="dale", passwd="iii", db="project", charset='utf8')
cursor = cnx.cursor()

'''------讀檔案的資料夾位置------'''
#mobile01
# contentDir = "E:/project/projectData/etl/mobile01/*/"
# titleDir = "E:/project/projectData/etl/mobile01/00_titles/"

#eprice
# contentDir = "E:/project/projectData/etl/eprice/L_G3_KZOOM_S5/*/"
# titleDir = "E:/project/projectData/etl/eprice/L_G3_KZOOM_S5/title00/"

#ptt
contentDir = "E:/project/projectData/etl/ptt/ppt/"
titleDir = "E:/project/projectData/etl/ptt/titles00/"

#module
moduleDir = "E:/project/projectData/etl/module/module.txt"

#------SQL們------
insert_title = "INSERT IGNORE INTO title (sourceWeb,webFirmNo,titleNo,URL,title) VALUES (%s, %s, %s, %s, %s) "
insert_title_Ptt = "INSERT IGNORE INTO title (sourceWeb,titleNo,URL,title) VALUES (%s, %s, %s, %s)"
insert_content = "INSERT IGNORE INTO content (sourceWeb,titleNo,contentNo,authorNo,author,postTime,content) VALUES (%s, %s, %s, %s, %s, %s, %s) "
insert_moduleTitle = "INSERT IGNORE INTO moduletitle (module,sourceWeb,titleNo) VALUES (%s, %s, %s) "
insert_module = "INSERT IGNORE INTO module (firm,module,size,weight,simCard,wDResists,cpu,ram,rom,memoryCard,communProtocol,duoSim,media,conn,sensor,battery,color,otherFunc) VALUES (%s , %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
insert_camera = "INSERT IGNORE INTO camera (module,main,minor,camOthers) values (%s ,%s ,%s ,%s)"
insert_screen = "INSERT IGNORE INTO screen (module,screenSize,resolution,screenOthers) values (%s ,%s ,%s ,%s)"
insert_jiebaCall = "INSERT IGNORE INTO jiabacall (moduleName,keyWord) values (%s ,%s)"
select = "SELECT %s FROM %s"

'''----------------------以下為把title或content的txt檔塞入資料庫的code(要用時把另一個先註解掉)-------------------------'''

'''把title塞進資料庫(eprice mobile)'''
# readTitle = glob.glob(titleDir+'*.txt') #讀取所文章的txt檔
# for titleFile in readTitle:
#     print titleFile
#     with io.open(titleFile, 'r', encoding='utf-8') as f:
#         for line in f:
#             titlein = line.split('\t')
#             #print len(titlein)
#             #print type(titlein[0])
#             #print titlein[0],titlein[1]
#             cursor.execute(insert_title,(titlein[2],titlein[3],titlein[4],titlein[5],titlein[6]))
#             print titlein[2]+"\t"+titlein[3]+"\t"+titlein[4]+"\t"+titlein[5]+"\t"+titlein[6]
#     print "---------------------------------------"

'''把title塞進資料庫(ptt)'''
# readTitle = glob.glob(titleDir+'*.txt') #讀取所文章的txt檔
# for titleFile in readTitle:
#     print titleFile
#     with io.open(titleFile, 'r', encoding='utf-8') as f:
#         for line in f:
#             titlein = line.split('\t')
#             #print len(titlein)
#             #print type(titlein[0])
#             #print titlein[0],titlein[1]
#             print titlein[1]+"\t"+titlein[2]+"\t"+titlein[4]+"\t"+titlein[5]
#             cursor.execute(insert_title_Ptt,(titlein[1],titlein[2],titlein[4],titlein[5]))
#
#     print "---------------------------------------"

'''把content塞進資料庫(mobile)'''
# readContent = glob.glob(contentDir + '*.txt')  #讀取所文章的txt檔
# for txtDir in readContent:
#     print txtDir
#     with io.open(txtDir, 'r', encoding='utf-8') as f:
#         page = 1
#         for line in f:
#             line = line.lstrip(BOM) #處理編碼問題
#             if page == 1:
#                 print line
#                 print page
#             else:
#                 contentin = line.split('\t')
#
#                 print "0+"+contentin[0] + "\t1+" + contentin[1] + "\t2+" + contentin[2] + "\t3+" + contentin[3] + "\t4+" + contentin[
#                     4] + "\t5+" + contentin[5] + "\t6+" + contentin[6]
#                 print page
#                 cursor.execute(insert_content, (
#                     contentin[0], contentin[1], contentin[2], contentin[3], contentin[4], contentin[5], contentin[6]))
#             page += 1
#         print "-------------------------------------"

'''把content塞進資料庫(eprice)'''
# readContent = glob.glob(contentDir + '*.txt')  #讀取所文章的txt檔
# for txtDir in readContent:
#     print txtDir
#     with io.open(txtDir, 'r', encoding='utf-8') as f:
#         page = 1
#         for line in f:
#             line = line.lstrip(BOM) #處理編碼問題
#             if page == 1:
#                 print line
#                 print page
#             else:
#                 contentin = line.split('\t')
#                 contentNo = contentin[3].split(" ")[0]
#                 date = contentin[4].split(" ")[0]
#                 print contentin[0] + "\t" + contentin[2] + "\t" + contentNo + "\t" + contentin[
#                     5] + "\t" + contentin[6] + "\t" + date + "\t" + contentin[7]
#                 print page
#                 cursor.execute(insert_content, (contentin[0], contentin[2], contentNo, contentin[5], contentin[6], date, contentin[7]))
#
#             page += 1
#         print "-------------------------------------"

'''把content塞進資料庫(ptt)'''
readContent = glob.glob(contentDir + '*.txt')  #讀取所文章的txt檔
#insert_content = "INSERT IGNORE INTO content (sourceWeb,titleNo,contentNo,authorNo,author,postTime,content) VALUES (%s, %s, %s, %s, %s, %s, %s) "

for txtDir in readContent:
    print txtDir
    with io.open(txtDir, 'r', encoding='utf-8') as f:

        for line in f:
            line = line.lstrip(BOM) #處理編碼問題
            contentin = line.split('\t')
            print contentin[0] + "\t" + contentin[1] + "\t" + contentin[3] + "\t" + contentin[4] + "\t" + contentin[4] + "\t" + contentin[5] + "\t" + contentin[6]

            cursor.execute(insert_content, (contentin[0], contentin[1], contentin[3] , contentin[4], contentin[4], contentin[5], contentin[6]))

        print "-------------------------------------"


'''-----------把module賽進資料庫-------------'''
# with io.open(moduleDir, 'r', encoding='utf-8') as f:
#     for line in f:
#         line = line.lstrip(BOM) #處理編碼問題
#         spec = line.split("\t")
#         print spec[0],"/",spec[1],"/",spec[2],"/",spec[3],"/",spec[7],"/",spec[8],"/",spec[9],"/",spec[10],"/",spec[11],"/",spec[12],"/",spec[13],"/",spec[14],"/",spec[18],"/",spec[19],"/",spec[20],"/",spec[21],"/",spec[22],"/",spec[23].strip()
#         cursor.execute(insert_module,(spec[0],spec[1],spec[2],spec[3],spec[7],spec[8],spec[9],spec[10],spec[11],spec[12],spec[13],spec[14],spec[18],spec[19],spec[20],spec[21],spec[22],spec[23].strip()))
#         print "-----------------------"
#         print spec[1],"/",spec[15],"/",spec[16],"/",spec[17]
#         cursor.execute(insert_camera,(spec[1],spec[15],spec[16],spec[17]))
#         print spec[1],"/",spec[4],"/",spec[5],"/",spec[6]
#         cursor.execute(insert_screen,(spec[1],spec[4],spec[5],spec[6]))
#         print "------------------------"




'''-------把moduleTitle連起來--------'''
# readTitle = glob.glob(titleDir+'*.txt') #讀取所文章的txt檔
# for titleFile in readTitle:
#     print titleFile
#     with io.open(titleFile, 'r', encoding='utf-8') as f:
#         for line in f:
#             line = line.lstrip(BOM)
#             titlein = line.split('\t')
#             print titlein[1],titlein[2],titlein[4]
#             cursor.execute(insert_moduleTitle,(titlein[1],titlein[2],titlein[4]))

'''-------把jiebacall塞進資料庫-------'''
# count = 0
# with io.open(moduleDir, 'r', encoding='utf-8') as f:
#     for line in f:
#         line = line.lstrip(BOM) #處理編碼問題
#         Name = line.split("\t")
#         cursor.execute(insert_jiebaCall,(Name[0],Name[1]))
#         count +=1
#         print count
#         print Name[0],Name[1]
#         print "-----------------------"
# print count


cnx.commit()
'''
cursor.execute(select,("*","content"))
for result in cursor:
    print result
'''

cursor.close()
cnx.close()

