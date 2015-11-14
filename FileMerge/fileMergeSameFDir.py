__author__ = 'Dale'
#同一資料夾存成一個檔
import glob;
import os;

#fileList = ['durability','battery','performance','operating','camera','storage','service','appearance','price_Buy','manuQuality','screen','softWare','hardWare','system','UI','sound','signal','GPS','compare','touch_keyboard','accessory','notPick']
dirLink = "G:/OneDrive/ETL/downloadFile/mi3/{0}"

#print 'osPath='+dirLink.format(title,'')
readResult = glob.glob(dirLink.format('*.txt'));
#print '-------------------------------'
opeFileAll = open(dirLink.format('mi3.txt'),'w');
for i in readResult:
    fileIn = open(i,'r');
    print i
    for line in fileIn.readlines():
        ele = line.split('\t')[1].strip();
        #print ele
        opeFileAll.write(ele+'\n');
    print '************end of write********************'
opeFileAll.close()