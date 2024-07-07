#!/usr/bin/python3
# -*- encoding = utf-8 -*-

'''
Utility of slicing BACI into smaller files per HS at a desired level instead of per year.
-------------------------
A: Xianja Ye
E: X[d0t]Ye[8]rug.nl
Groningen Growth & Development Centre
University of Groningen
-------------------------

To use: 
Need to have python 3.* installed.

Put this code in a folder. Create a subfolder, e.g. BACI_RAW, to store the raw
BACI csv data files from CEPII.fr. 

Adjust the "filename_lead", "filename_end" and start/end years in the code that
fit with the data. 

In system shell (e.g. cmd.exe in windows), go to the folder with this code and
the subfolder of BACI, Then type 
python HSSplit_4d.py
to create sliced CSV files. 

They will be named as HS4_****.csv in the same folder, in the end there will be
also a HSn_LIST.csv file created, which is about all the HS code at [n] level entries 
that have appeared in the version of BACI. The value n vary across 1 to 6. 
'''

print("Initializing...");


data_location = 'BACI_RAW'

filename_lead = 'BACI_HS07_Y'
filename_end =  '_V202401.csv'
startyear = 2007
endyear = 2022

# Number of HS digits. The value must between 1 and 6.
n = 6

# Cache size per each file operation, 
# Note about trade-offs: 
# Larger number = lower frequency of file writing operations
#                 but more memory usage, 

# Takes about 400MB when set to 5000.
cachesize_std = 3000;

cachesize_hs = int(3000*(7-n/2));


import os;
os.chdir(data_location);

import gc;
gc.enable();

import time;
time0 = time.time();

def printtime():
    time1 = time.time();
    chg = time1-time0;
    mins = int(chg/60);
    secs = int(chg - 60*mins);
    print("%02d:%02d" %(mins, secs));



def line_appending(cache, target, dt):
    if target in cache.keys():
        cache[target].append(dt);
        if len(cache[target]) > cachesize_hs:
            write_to_file(target, cache[target]);
            # cache.update({target:[]});
            del cache[target][:];
            # gc.collect();
    else:
        create_file(target);
        cache.update({target:[dt]});

def cache_allwrite(cache):
    for hs in cache.keys():
        if len(cache[hs])>0:
            write_to_file(hs, cache[hs]);
            del cache[hs][:];
            # gc.collect();

def makelist(cache):
    HS4_List = sorted(cache.keys());
    g = open('HS4_LIST.csv', 'w'); 
    g.writelines('HS4_Code\n');
    txt = '\n'.join(HS4_List);
    g.writelines(txt);
    g.close();

def create_file(target):
    filename = 'HS'+str(len(target))+'_'+target+'.csv';
    g=open(filename, 'w');
    g.writelines('y,i,j,k,v,q\n');
    g.close();

def write_to_file(target, txt):
    filename = 'HS'+str(len(target))+'_'+target+'.csv';
    g=open(filename, 'a');
    g.writelines(txt);
    g.close();




cache_host = dict({})


# Begin Operation
print("Processing BACI files. It may takes a while.")
print("")
print("------------------------")
print(" Year | Total Time Used ")
print("------------------------")
for yr in range(startyear, endyear +1):
    print(" %4d |    " % yr, end="", flush=True);
    filename = filename_lead + str(yr) + filename_end;
    f = open(filename, 'r')
    # skip the first line
    aline = f.readline()
    aline = f.readline()
    
    while len(aline)>5:
        lineinfo = aline.split(',');
        [yy, ii, jj, kk, vv, qq] = lineinfo;
        dt = ','.join([yy, ii, jj, kk, vv.strip(), qq.strip()])+'\n';
        kn = kk.strip()[:n];
        line_appending(cache_host, kn, dt);
        aline = f.readline();

    f.close();
    printtime();


# Finalizing, write out all remaining data in the cache
print("------------------------")
print("Finalizing, please wait....")
cache_allwrite(cache_host);
makelist(cache_host);
print("Total time used: ", end ="")
printtime();
