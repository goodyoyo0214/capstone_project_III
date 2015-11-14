
# coding: utf-8


import glob;
import os;
fileList = ['durability','battery','performance','operating','camera','storage','service','appearance','price_Buy','manuQuality','screen','softWare','hardWare','system','UI','sound','signal','GPS','compare','touch_keyboard','accessory','notPick']
dirLink = "G:/OneDrive/ETL/downloadFile/merge/{0}{1}"
for title in fileList:
    #print 'osPath='+dirLink.format(title,'')
    readResult = glob.glob(dirLink.format(title,'/*.txt'));
    print 'read='+dirLink.format(title,'/*.txt')        
    print 'write='+dirLink.format(title,'/shing.txt')
    #print '-------------------------------'
    opeFileAll = open(dirLink.format(title,'/shing.txt'),'w');
    for i in readResult:
        fileIn = open(i,'r');
        print i
        for line in fileIn.readlines():
            opeFileAll.write(line);
    print '************end of write********************'
    opeFileAll.close()





