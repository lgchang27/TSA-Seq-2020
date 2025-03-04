#!/usr/bin/python
# Programmer : Liguo Zhang
# Date: 20191217

'''
Take the _mergeAdjacent.bed file for the changed domains, add other values, always cell2-cell1
Output bed format: chr  start  end  cell1_percentile  cell2_percentile  cell2-cell1_percentile
Take replicate mean
Only keep domains above a threshold
'''

import os,sys,argparse
from TSA_utility import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-b','--bed',type=str,dest="bed",help="bed file ")
    p.add_argument('-p1','--perc1',type=str,dest="perc1",help="percentile file1 (cell line 1 replicate 1)")
    p.add_argument('-p2','--perc2',type=str,dest="perc2",help="percentile file2 (cell line 1 replicate 2)")
    p.add_argument('-p3','--perc3',type=str,dest="perc3",help="percentile file3 (cell line 2 replicate 1)")
    p.add_argument('-p4','--perc4',type=str,dest="perc4",help="percentile file4 (cell line 2 replicate 2)")
    p.add_argument('-g','--genome',type=str,dest="genome",help="genome file")
    p.add_argument('-o','--output',type=str,dest="output",help="output file name")
    return p.parse_args()

def CollectValue(wigfile):
    hash={}
    array=[]
    num=1
    all=[]
    for line in ReadFromFile(wigfile):
        if line.strip().startswith('#') or line.strip() == '' or line.strip() == '\n':
            continue
        row = line.strip().split()
        if row[0] == 'track':
            continue
        num += 1
        if row[0] == 'variableStep': # new track chrom begin
            if len(array)!=0:
                if chrom != row[1].split('=')[1]:
                    hash[chrom]=array
                    array=[]
            chrom = row[1].split('=')[1]
        else:
            array.append((row[0],row[1]))
            all.append(float(row[1]))
        hash[chrom]=array
    print "all value num:"+str(len(all))
    print "max vallue:"+str(max(all))
    print "min vallue:"+str(min(all))
    return hash


def Main():
    global args
    args=ParseArg()
    perc_hash1 = CollectValue (args.perc1)
    perc_hash2 = CollectValue (args.perc2)
    perc_hash3 = CollectValue (args.perc3)
    perc_hash4 = CollectValue (args.perc4)
    newBed=WriteToFile(args.output+".bed")
    newBed1=WriteToFile(args.output+"_browser.bed")
    
    '''read bed file'''
    chrom=None
    for line in ReadFromFile(args.bed):
        row = line.strip().split()
        chrom = row[0]
        start = row[1]
        end = row[2]
        perc_list1 = perc_hash1 [chrom]
        perc_list2 = perc_hash2 [chrom]
        perc_list3 = perc_hash3 [chrom]
        perc_list4 = perc_hash4 [chrom]
        array1 = []
        array2 = []
        array3 = []
        array4 = []
        for i in range (len(perc_list1)):
            if int(perc_list1[i][0]) >= int(start) and int(perc_list1[i][0]) < int(end):
                array1.append(float(perc_list1[i][1]))
        #print array1
        for j in range (len(perc_list2)):
            if int(perc_list2[j][0]) >= int(start) and int(perc_list2[j][0]) < int(end):
                array2.append(float(perc_list2[j][1]))
        #print array2
        for m in range (len(perc_list3)):
            if int(perc_list3[m][0]) >= int(start) and int(perc_list3[m][0]) < int(end):
                array3.append(float(perc_list3[m][1]))
        #print array3
        for n in range (len(perc_list4)):
            if int(perc_list4[n][0]) >= int(start) and int(perc_list4[n][0]) < int(end):
                array4.append(float(perc_list4[n][1]))
        #print array4
        if len(array1) != len(array2):
            print "error"
        if len(array1) != len(array3):
            print "error"
        if len(array1) != len(array4):
            print "error"
        cell1rep1 = np.mean(array1)+50
        cell1rep2 = np.mean(array2)+50
        cell2rep1 = np.mean(array3)+50
        cell2rep2 = np.mean(array4)+50
        cell1 = (cell1rep1+cell1rep2)/2
        cell2 = (cell2rep1+cell2rep2)/2
        percentileRsd = cell2 - cell1   
        #print percentileRsd
        if cell2 >= 95:
            print >>newBed, "%s\t%s\t%s\t%f\t%f\t%f" % (chrom, start, end, cell1, cell2, percentileRsd)
            print >>newBed1, "%s\t%s\t%s\t%f" % (chrom, start, end, percentileRsd) 
    newBed.flush()
    newBed1.flush()

    sort="sort -k1,1 -k2,2n %s > %s" % (args.output+"_browser.bed", args.output+"_browser.sorted.bed")
    bed2bb = "utilities/bedToBigBed %s %s %s" % ( args.output+'_browser.sorted.bed', args.genome, args.output+'_browser.bb')
    os.system(sort)
    os.system(bed2bb)


if __name__=="__main__":
    Main()
