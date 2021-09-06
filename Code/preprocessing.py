#This file is an example of preprocessing data in 0021500473.json, dealing with otherfiles are similar.
#set environment
import os
import pandas as pd
import numpy as np
L1 = '/Users/shentao/Desktop/Analysis on Dymanics of Poession Behavior based on MDP/raw data'
os.chdir(L1)

#load data and apply transformation
import json

f = open('0021500473.json', 'r+')
str_json = f.read()

temp = json.loads(str_json) 

#basic data
gameid = temp['gameid']
gamedate = temp['gamedate']
events=temp['events']

#data cleaning
alldata=[]
for i in range(0,len(events)):
    for j in range(0,len(events[i]['moments'])):
        alldata.append(events[i]['moments'][j])
        
#new data setting
newl = []
for i in alldata:
    if i not in newl:
        newl.append(i)

#br is a round based new data
l1=[]
br=[]
for i in range(0,len(newl)-1):
    time0 = newl[i-1][3]
    time1 = newl[i][3]
    time2 = newl[i+1][3]
    if (time0 and time1 and time2) != None:
        if (time1>=23.8) and (time1>time0):
            br.append(l1)
            l1=[]


        else:

            l1.append(newl[i])

#judge the ball carrier
from math import *
dat=[]
chi=[]
a=0
for i in range(0,len(br)):
    for j in range(0,len(br[i])):
        if br[i][j][5][0][0]==-1:
            xball = br[i][j][5][0][3]
            yball = br[i][j][5][0][4]
            if len(br[i][j][5])==11:
                dislist=[]
                for k in range(1,11):
                    dis = sqrt((br[i][j][5][k][3]-xball)**2+(br[i][j][5][k][4]-yball)**2)
                    dislist.append(dis)
                mindist=min(dislist)
                minindex=dislist.index(mindist)

                if mindist<3.2:
                   
                    player=br[i][j][5][minindex+1]
                    l=[br[i][j],player]
                    dat.append(l)
                    #print(i,j,player)
                    a=a+1
                else:
                    l=[br[i][j],None]
                    dat.append(l)

    chi.append(dat)
    dat=[]

#judge the passing behavior
chuanqiu=[]
kk=[]
for i in range(0,len(chi)):
    for j in range(0,len(chi[i])):
        if chi[i][j][1] != None:
            kk.append(chi[i][j])
        
    chuanqiu.append(kk)
    kk=[]
    
    
#select data with only ball passing
zhichuanqiu=[]
zzz=[]

for i in range(0,len(chuanqiu)):
    for j in range(0,(len(chuanqiu[i])-1)):
        team0 = chuanqiu[i][j][1][0]
        team1 = chuanqiu[i][j+1][1][0]
        player0 = chuanqiu[i][j][1][1]
        player1 = chuanqiu[i][j+1][1][1]
        if (team0 == team1) and (player0 != player1):
            if chuanqiu[i][j][0][2]-chuanqiu[i][j+1][0][2]<1:
                guo = [chuanqiu[i][j][0][0],chuanqiu[i][j][0][2],chuanqiu[i][j][0][3],chuanqiu[i][j][1],chuanqiu[i][j+1][1]]
                lla = [chuanqiu[i][j],guo]
                zzz.append(lla)
    zhichuanqiu.append(zzz)
    zzz=[]
    
#judge whether shooting has happened
tl=[]
for i in chi:
    tl.append(i)
    

a111=0
zhitoulan=[]
aaaa=[]
jlist=[]
for i in range(0,len(tl)):
    for j in range(0,len(tl[i])):
        if tl[i][j][0][5][0][0]==-1:
            if tl[i][j][0][5][0][4]>10:
                if (tl[i][j][0][5][0][3]>24) and (tl[i][j][0][5][0][3]<26):
                    if (tl[i][j][0][5][0][2]>84) or(tl[i][j][0][5][0][2]<10):
                        if tl[i][j][0][3]<23:
                            jlist.append(j)
                            #print(i,j,tl[i][j][0][3],tl[i][j][0][5][0],tl[i][j][1])
    if jlist != []:
        minj=min(jlist)
        jlist=[]
        #print(minj)
        for k in range(minj,0,-1):
            if tl[i][k][1] != None:
                aaaa = [tl[i][k],'shot']
                a111+=1
                break
    zhitoulan.append(aaaa)
    aaaa=[]

#combine the ball passing and shooting data together
touc=[]
tc=[]

for i in range(0,len(br)):
    if zhichuanqiu[i] == []:
        if zhitoulan[i] != []:
            tc.append(zhitoulan[i])
            touc.append(tc)
            tc=[]
            continue 
    if zhitoulan[i] != []:  
        for j in range(0,len(zhichuanqiu[i])):
            if zhichuanqiu[i][j][0][0][2]>zhitoulan[i][0][0][2]:
                tc.append(zhichuanqiu[i][j])
        tc.append(zhitoulan[i])
        touc.append(tc)
        tc=[]

#select data from CLE
cletouc=[]
for i in range(0,len(touc)):
    a=len(touc[i])
    b=touc[i][a-1]
    c=b[0][1][0]
    if c==1610612739:
        cletouc.append(touc[i])

#compute the defensive conditions
l01=[]
kak=[]
cletoucf=[]
for i in range(0,len(cletouc)):
    for j in range(0,len(cletouc[i])):
        info = cletouc[i][j][0][0][5]
        team = 1610612739
        for k in range(1,11):
            if info[k][0] == team:
                x0=info[k][2]
                y0=info[k][3]
                dislist=[]
                for w in range(1,11):
                    if info[w][0] != team:
                        x1 = info[w][2]
                        y1 = info[w][3]
                        dis = sqrt((x0-x1)**2+(y0-y1)**2)
                        dislist.append(dis)
                mindist=min(dislist)
                if mindist<4:
                    l01.append(1)    
                else:
                    l01.append(0)
        guoguo=[cletouc[i][j],l01]
        kak.append(guoguo)
        #print(l01)
        l01=[]
    cletoucf.append(kak)
    kak=[]
                            
                      
#judge the region the ball carrier standing on 
rar=[]
cletoucfr=[]

for i in range(0,len(cletoucf)):
    for j in range(0,len(cletoucf[i])):
        info = cletoucf[i][j][0][0][1]
        xa = info[2]
        ya = info[3]
        
        if (xa<15.6) and (ya<16.6):
            r=1
        elif (xa>15.6) and (ya<16.6) and (xa<31.2):
            r=2
        elif (ya<16.6) and (xa>31.2) and(xa<47):
            r=3
        elif (xa>47) and (ya<16.6) and (xa<62.6):
            r=11
        elif (ya<16.6) and (xa>62.6) and(xa<78.2):
            r=22
        elif (xa>78.3) and (ya<16.6) and (xa<94):
            r=33
            
        elif (ya>16.6) and (ya<33.2) and (xa<15.6):
            r=4
        elif (ya>16.6) and (ya<33.2) and (xa>15.6) and(xa<31.2):
            r=5
        elif (ya>16.6) and (ya<33.2) and (xa>31.2) and(xa<47):
            r=6
        elif (ya>16.6) and (ya<33.2) and (xa>47) and(xa<62.6):
            r=44
        elif (ya>16.6) and (ya<33.2) and (xa>62.6) and(xa<78.2):
            r=55
        elif (ya>16.6) and (ya<33.2) and (xa>78.2) and(xa<94):
            r=66
        
        elif (ya>33.2) and (ya<50) and (xa<15.6):
            r=7
        elif (ya>33.2) and (ya<50) and (xa>15.6) and(xa<31.2):
            r=8
        elif (ya>33.2) and (ya<50) and (xa>31.2) and(xa<47):
            r=9
        elif (ya>33.2) and (ya<50) and (xa>47) and(xa<62.6):
            r=77
        elif (ya>33.2) and (ya<50) and (xa>62.6) and(xa<78.2):
            r=88
        elif (ya>33.2) and (ya<50) and (xa>78.2) and(xa<94):
            r=99
        
        guoguoguo=[cletoucf[i][j],r]
        rar.append(guoguoguo)
        #print(r)

    cletoucfr.append(rar)
    rar=[]
                
#final preprocessed data collection 
zhengli=[]
for i in range(0,len(cletoucfr)):
    for j in range(0,len(cletoucfr[i])):
        if cletoucfr[i][j][0][0][0][1][0] != 1610612739:
            continue
        huihe = i+1
        region = cletoucfr[i][j][1]
        defense = cletoucfr[i][j][0][1]
        if cletoucfr[i][j][0][0][1] == 'shot':
            sop = 'shot'
            person2 = None
            xp2 = None
            yp2 = None
            score = '?'
        else:
            sop = 'pass'
            person2 = cletoucfr[i][j][0][0][1][4][1]
            xp2 = cletoucfr[i][j][0][0][1][4][2]
            yp2 = cletoucfr[i][j][0][0][1][4][3]
            score = 0
            
            
        time = cletoucfr[i][j][0][0][0][0][2]
        quarter = cletoucfr[i][j][0][0][0][0][0]
        qtime = cletoucfr[i][j][0][0][0][0][3]
        person = cletoucfr[i][j][0][0][0][1][1]
        team = cletoucfr[i][j][0][0][0][1][0]
        xp = cletoucfr[i][j][0][0][0][1][2]
        yp = cletoucfr[i][j][0][0][0][1][3]
        
        al = [huihe,time,quarter,qtime,sop,team,person,xp,yp,region,defense,person2,xp2,yp2,score]
        zhengli.append(al)
        
#round-based data transformation
zhenghe = []
aa=[]
huihe=1

for i in range(0,len(zhengli)):
    if zhengli[i][0] == huihe:
        aa.append(zhengli[i])
    else:
        zhenghe.append(aa)
        aa=[]
        aa.append(zhengli[i])
        huihe += 1
        
#select episodes with consecutive possession behaviors > 3
shai=[]
a=[]
for i in range(0,len(zhenghe)):
    lenne = len(zhenghe[i])-1   
    if lenne == 0:
        continue
    else:
        a.append(zhenghe[i][lenne])
        for j in range(lenne,0,-1):
            p1 = zhenghe[i][j][6]
            p2 = zhenghe[i][j-1][11]
            if p1 == p2:
                a.append(zhenghe[i][j-1])
            else:
                break
        if len(a)==1:
            a=[]
            continue
        else:
            a.reverse()
            if a != []:
                shai.append(a)
                a=[]
            
zanshi=[]
for i in range(0,len(shai)):
    for j in range(0,len(shai[i])):
        zanshi.append(shai[i][j])

#store the data into csv file
name = ['huihe','time','quarter','qtime','sop','team','person','xp','yp','region','defense','person2','xp2','yp2','score']
import pandas as pd
test=pd.DataFrame(columns=name,data=zanshi)
test.to_csv('20151229.csv',encoding='gbk')