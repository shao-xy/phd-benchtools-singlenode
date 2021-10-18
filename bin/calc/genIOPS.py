#!/usr/bin/env python3

import sys
import os
#DirPrefix = "log-hash-100client-5node-5mds/"
DirPrefix = sys.argv[1]
IOPSPrefix = "IOPS-mds"
Suffix = "-minute"
inodeList = []
inodeMinuteList = []
count = 0

thisBatchList = ["0","1","2","3","4"]
#thisBatchList = ["10","13"]
tailBatchList = [""]
#thisBatchList = ["3"]
for thisBatch in thisBatchList:
    for tailBatch in tailBatchList:
        inodeList = []
        inodeMinuteList = []
        with open(DirPrefix+IOPSPrefix+thisBatch+tailBatch, 'r') as inodeFile:
            for line in inodeFile:
                inodeList.append(int(line.strip("\n", )))
        #print(inodeList)
        #print(len(inodeList))
        pos = 0
        thisMintue = 0
        for inode in inodeList:
            if pos == 60:
                pos = 0
                thisMintue += inode
                inodeMinuteList.append(thisMintue//60)
                thisMintue = 0
            else:
                thisMintue += inode
            pos+=1

        if pos != 0:
            inodeMinuteList.append(thisMintue // pos)

        print(inodeMinuteList)
        print(len(inodeMinuteList))

        pos = 0
        with open(DirPrefix+IOPSPrefix+thisBatch+tailBatch+Suffix, 'w') as inodeMinuteFile:
            for i in inodeMinuteList:
                inodeMinuteFile.write(str(pos)+" "+str(inodeMinuteList[pos])+"\n")
                pos+=1
