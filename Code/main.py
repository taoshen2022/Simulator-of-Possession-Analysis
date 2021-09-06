import os
import pandas as pd
import numpy as np
import random

#Part one:
#After data preprocessing, we have four csv each represented a layer slice
#Then we will read the data and store them into lists
#The path should be redesigned as the path storing the csv 1,2,3,4.
L1 = '/Users/shentao/Desktop/Analysis on Dymanics of Poession Behavior based on MDP/raw data'
os.chdir(L1)

#导入数据，并改变数据格式
df1 = pd.read_table("1.csv",sep=",")
df2 = pd.read_table("2.csv",sep=",")
df3 = pd.read_table("3.csv",sep=",")
df4 = pd.read_table("4.csv",sep=",")

dfnp1 = np.array(df1)
dfnp2 = np.array(df2)
dfnp3 = np.array(df3)
dfnp4 = np.array(df4)

data1 = dfnp1.tolist()
data2 = dfnp2.tolist()
data3 = dfnp3.tolist()
data4 = dfnp4.tolist()

zhenghe1 = []
aa=[]
huihe=1

for i in range(0,len(data1)):
    if data1[i][0] == huihe:
        aa.append(data1[i])
    else:
        zhenghe1.append(aa)
        aa=[]
        aa.append(data1[i])
        huihe += 1
zhenghe1.append(aa)

zhenghe2 = []
aa=[]
huihe=1

for i in range(0,len(data2)):
    if data2[i][0] == huihe:
        aa.append(data2[i])
    else:
        zhenghe2.append(aa)
        aa=[]
        aa.append(data2[i])
        huihe += 1
zhenghe2.append(aa)

zhenghe3 = []
aa=[]
huihe=1

for i in range(0,len(data3)):
    if data3[i][0] == huihe:
        aa.append(data3[i])
    else:
        zhenghe3.append(aa)
        aa=[]
        aa.append(data3[i])
        huihe += 1
zhenghe3.append(aa)

zhenghe4 = []
aa=[]
huihe=1

for i in range(0,len(data4)):
    if data4[i][0] == huihe:
        aa.append(data4[i])
    else:
        zhenghe4.append(aa)
        aa=[]
        aa.append(data4[i])
        huihe += 1
zhenghe4.append(aa)

#boostrapping steps to construct synthetic data
boot1 = []
for i in range(100):
    boot1.append(np.floor(np.random.random()*len(zhenghe1)))

D1 = []
for i in range(100):
    D1.append(zhenghe1[int(boot1[i])])

boot2 = []
for i in range(100):
    boot2.append(np.floor(np.random.random()*len(zhenghe2)))

D2 = []
for i in range(100):
    D2.append(zhenghe2[int(boot2[i])])

boot3 = []
for i in range(100):
    boot3.append(np.floor(np.random.random()*len(zhenghe3)))

D3 = []
for i in range(100):
    D3.append(zhenghe3[int(boot3[i])])

boot4 = []
for i in range(100):
    boot4.append(np.floor(np.random.random()*len(zhenghe4)))

D4 = []
for i in range(100):
    D4.append(zhenghe4[int(boot4[i])])

#Part two: construct lists of episodes and dictionary of states
#output: sample1-4, v_dic, q_dic, v_q _indicator(index dictionary of value function and q function)
def construct_sample(D):
    result = []
    for i in range(len(D)):
        result.append([])
        for j in D[i]:
            if j[4] == 'pass':
                 result[i].append([j[6],j[9],j[10],0,j[14]])
            else:
                 result[i].append([j[6],j[9],j[10],1,j[14]])
           
    return result

def list_defence():
    result = []
    for i in range(2):
         for j in range(2):
              for k in range(2):
                   for l in range(2):
                        for m in range(2):
                            result.append([i,j,k,l,m])
    return result

sample1 = construct_sample(D1)
sample2 = construct_sample(D2)
sample3 = construct_sample(D3)
sample4 = construct_sample(D4)

player = [201567,2592,2747,203521,203099,202681,202697,202684,201619,2760,202389,2544,2210,2590]
region = [1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99]
defence = list_defence()
action = [0,1]
q_dic = {}
v_dic = {}
v_q_indicator = []
v_num = 1
q_num = 1
for i in player:
    for j in region:
        for k in defence:
            v_dic[str([i,j,str(k)])] = v_num
            v_q_indicator.append([v_num-1])
            v_num += 1
            for m in action:
                q_dic[str([i,j,str(k),m])] = q_num
                v_q_indicator[len(v_q_indicator)-1].append(q_num-1)
                q_num += 1
                

#Part three:
#PBE algorithm with td learning

def td_learning(q_dic,q_num,v_dic,v_num,gamma,alpha,sample):
    Q = np.random.random([q_num-1,1])
    V = np.random.random([v_num-1,1])
    for i in sample:
        for j in range(len(i)-1):
            Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] =  Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] + alpha*(i[j][4]+gamma*Q[q_dic[str([i[j+1][0],i[j+1][1],i[j+1][2],i[j+1][3]])],0]-Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0])
            V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0] =  V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0] + alpha*(i[j][4]+gamma*V[v_dic[str([i[j+1][0],i[j+1][1],i[j+1][2]])],0]-V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0])
        Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] =  Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] + alpha*(i[j][4]+gamma*0-Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0])
        V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0] =  V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0] + alpha*(i[j][4]+gamma*0-V[v_dic[str([i[j][0],i[j][1],i[j][2]])],0])                                                                                                                   
    return V,Q
    

def policy_estimation(V,Q,v_q_indicator):
    pi = np.zeros([np.size(V,0),2])
    for i in v_q_indicator:
        pi[i[0],0] = (V[i[0],0]-Q[i[2],0])/(Q[i[1],0]-Q[i[2],0])
        pi[i[0],1] = 1-pi[i[0],0]
    return pi

def identity_vector(player,name):
    result = []
    for i in range(len(player)):
        result.append(0)
    result[player.index(name)] = 1
    return result

def construct_phi(q_dic,q_num,v_dic,v_num,player,region,v_q_indicator,pi):
    Q = np.zeros([q_num-1,38])
    V = np.zeros([v_num-1,38])
    for i in range(q_num-1):
        j = q_dic[i+1]
        if j[0] in player:
            Q[i,player.index(j[0])] = 1
        if j[1] in region:
            Q[i,region.index(j[1])+14] = 1
        Q[i,32] = int(j[2][1])
        Q[i,33] = int(j[2][4])
        Q[i,34] = int(j[2][7])
        Q[i,35] = int(j[2][10])
        Q[i,36] = int(j[2][13])
        Q[i,37] = int(j[3])
    for k in v_q_indicator:
        V[k[0],:] = pi[k[0],0]*Q[k[1],:]+pi[k[0],1]*Q[k[2],:]
    return V,Q

#get V Q and pi from td learning
V1, Q1 = td_learning(q_dic=q_dic,q_num=q_num, v_dic=v_dic,v_num=v_num, gamma=0.9, alpha=0.1, sample=sample1)
pi1 = policy_estimation(V=V1, Q=Q1, v_q_indicator=v_q_indicator)
V2, Q2 = td_learning(q_dic=q_dic,q_num=q_num, v_dic=v_dic,v_num=v_num, gamma=0.9, alpha=0.1, sample=sample2)
pi2 = policy_estimation(V=V2, Q=Q2, v_q_indicator=v_q_indicator)
V3, Q3 = td_learning(q_dic=q_dic,q_num=q_num, v_dic=v_dic,v_num=v_num, gamma=0.9, alpha=0.1, sample=sample3)
pi3 = policy_estimation(V=V3, Q=Q3, v_q_indicator=v_q_indicator)
V4, Q4 = td_learning(q_dic=q_dic,q_num=q_num, v_dic=v_dic,v_num=v_num, gamma=0.9, alpha=0.1, sample=sample4)
pi4 = policy_estimation(V=V4, Q=Q4, v_q_indicator=v_q_indicator)

#construct q_dic2 and v_dic2, this time the keys and values are reversed
q_dic2 = {}
v_dic2 = {}
v_num2 = 1
q_num2 = 1
for i in player:
    for j in region:
        for k in defence:
            v_dic2[v_num2] = [i,j,str(k)]
            v_num2 += 1
            for m in action:
                q_dic2[q_num2] = [i,j,str(k),m]
                q_num2 += 1
                
#Obtain feature vector phi, then apply LSTD on each layer slice
phi_v1, phi_q1 = construct_phi(q_dic2,q_num,v_dic2,v_num,player,region,v_q_indicator,pi1)
phi_v1 = np.transpose(phi_v1)
phi_q1 = np.transpose(phi_q1)
M1 = np.full([38,38],0.01)
N1 = np.full([38,1],0.01)
gamma = 0.9
for k in range(2):
    for i in sample1:
        for j in range(len(i)-1):
            x = np.array([[m[v_dic[str([i[j+1][0],i[j+1][1],i[j+1][2]])]-1] for m in phi_v1]]).transpose()
            y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q1]]).transpose()
            M1 = M1 + np.dot(x,y.transpose()/gamma-x.transpose())
            N1 = N1 + x*i[j][4]/gamma
        x = np.array([[m[v_dic[str([i[j][0],i[j][1],i[j][2]])]-1] for m in phi_v1]]).transpose()
        y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q1]]).transpose()
        M1 = M1 + np.dot(x,y.transpose()/gamma-x.transpose())
        N1 = N1 + x*i[j][4]/gamma
    
    theta1 = np.dot(np.linalg.inv(M1),N1)

phi_v2, phi_q2 = construct_phi(q_dic2,q_num,v_dic2,v_num,player,region,v_q_indicator,pi2)
phi_v2 = np.transpose(phi_v2)
phi_q2 = np.transpose(phi_q2)
M2 = np.full([38,38],0.01)
N2 = np.full([38,1],0.01)
gamma = 0.9
for k in range(150):
    for i in sample2:
        for j in range(len(i)-1):
            x = np.array([[m[v_dic[str([i[j+1][0],i[j+1][1],i[j+1][2]])]-1] for m in phi_v2]]).transpose()
            y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q2]]).transpose()
            M2 = M2 + np.dot(x,y.transpose()/gamma-x.transpose())
            N2 = N2 + x*i[j][4]/gamma
        x = np.array([[m[v_dic[str([i[j][0],i[j][1],i[j][2]])]-1] for m in phi_v2]]).transpose()
        y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q2]]).transpose()
        M2 = M2 + np.dot(x,y.transpose()/gamma-x.transpose())
        N2 = N2 + x*i[j][4]/gamma
    
    theta2 = np.dot(np.linalg.inv(M2),N2)

phi_v3, phi_q3 = construct_phi(q_dic2,q_num,v_dic2,v_num,player,region,v_q_indicator,pi3)
phi_v3 = np.transpose(phi_v3)
phi_q3 = np.transpose(phi_q3)
M3 = np.full([38,38],0.01)
N3 = np.full([38,1],0.01)
gamma = 0.9
for k in range(150):
    for i in sample3:
        for j in range(len(i)-1):
            x = np.array([[m[v_dic[str([i[j+1][0],i[j+1][1],i[j+1][2]])]-1] for m in phi_v3]]).transpose()
            y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q3]]).transpose()
            M3 = M3 + np.dot(x,y.transpose()/gamma-x.transpose())
            N3 = N3 + x*i[j][4]/gamma
        x = np.array([[m[v_dic[str([i[j][0],i[j][1],i[j][2]])]-1] for m in phi_v3]]).transpose()
        y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q3]]).transpose()
        M3 = M1 + np.dot(x,y.transpose()/gamma-x.transpose())
        N3 = N1 + x*i[j][4]/gamma
    
    theta3 = np.dot(np.linalg.inv(M3),N3)

phi_v4, phi_q4 = construct_phi(q_dic2,q_num,v_dic2,v_num,player,region,v_q_indicator,pi4)
phi_v4 = np.transpose(phi_v4)
phi_q4 = np.transpose(phi_q4)
M4 = np.full([38,38],0.01)
N4 = np.full([38,1],0.01)
gamma = 0.9
for k in range(150):
    for i in sample4:
        for j in range(len(i)-1):
            x = np.array([[m[v_dic[str([i[j+1][0],i[j+1][1],i[j+1][2]])]-1] for m in phi_v4]]).transpose()
            y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q4]]).transpose()
            M4 = M4 + np.dot(x,y.transpose()/gamma-x.transpose())
            N4 = N4 + x*i[j][4]/gamma
        x = np.array([[m[v_dic[str([i[j][0],i[j][1],i[j][2]])]-1] for m in phi_v4]]).transpose()
        y = np.array([[m[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])]-1] for m in phi_q4]]).transpose()
        M4 = M4 + np.dot(x,y.transpose()/gamma-x.transpose())
        N4 = N4 + x*i[j][4]/gamma

    theta4 = np.dot(np.linalg.inv(M4),N4)

#Final estimation results
Q11 = np.dot(phi_q1.transpose(),theta1)
Q22 = np.dot(phi_q2.transpose(),theta2)
Q33 = np.dot(phi_q3.transpose(),theta3)
Q44 = np.dot(phi_q4.transpose(),theta4)
V11 = np.zeros([8064,1])
V22 = np.zeros([8064,1])
V33 = np.zeros([8064,1])
V44 = np.zeros([8064,1])
for k in v_q_indicator:
     V11[k[0],0] = pi1[k[0],0]*Q11[k[1],0]+pi1[k[0],1]*Q11[k[2],0]
     V22[k[0],0] = pi2[k[0],0]*Q22[k[1],0]+pi2[k[0],1]*Q22[k[2],0]
     V33[k[0],0] = pi3[k[0],0]*Q33[k[1],0]+pi3[k[0],1]*Q33[k[2],0]
     V44[k[0],0] = pi4[k[0],0]*Q44[k[1],0]+pi4[k[0],1]*Q44[k[2],0]
     
#Typical mse presentation
print(np.sum([num*num for num in (Q22-Q2/10)])/16128)
print(np.sum([num*num for num in (Q44-Q4/10)])/16128)
print(np.sum([num*num for num in (V22-V2/10)])/8064)
print(np.sum([num*num for num in (V44-V4/10)])/8064)

#Part four:
#PBI algorithm with q learning
def q_learning(q_dic,q_num,v_num,v_q_indicator,gamma,alpha,sample):
    Q = np.random.random([q_num-1,1])
    pi = np.zeros([v_num-1,2])
    for k in v_q_indicator:
        if Q[k[1],0] >= Q[k[2],0]:
            pi[k[0],0] = 1
        else:
            pi[k[0],1] = 1
    for i in sample:
        for j in range(len(i)-1):
            Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] =  Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] + alpha*(i[j][4]+gamma*max(Q[q_dic[str([i[j+1][0],i[j+1][1],i[j+1][2],0])],0],Q[q_dic[str([i[j+1][0],i[j+1][1],i[j+1][2],1])],0])-Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0])
        Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] =  Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0] + alpha*(i[j][4]+gamma*0-Q[q_dic[str([i[j][0],i[j][1],i[j][2],i[j][3]])],0])
    return Q,pi

Q_im1, pi_im1 = q_learning(q_dic=q_dic, q_num=q_num, v_num=v_num, v_q_indicator=v_q_indicator, gamma=0.9, alpha=0.1, sample=sample1)
Q_im2, pi_im2 = q_learning(q_dic=q_dic, q_num=q_num, v_num=v_num, v_q_indicator=v_q_indicator, gamma=0.9, alpha=0.1, sample=sample2)
Q_im3, pi_im3 = q_learning(q_dic=q_dic, q_num=q_num, v_num=v_num, v_q_indicator=v_q_indicator, gamma=0.9, alpha=0.1, sample=sample3)
Q_im4, pi_im4 = q_learning(q_dic=q_dic, q_num=q_num, v_num=v_num, v_q_indicator=v_q_indicator, gamma=0.9, alpha=0.1, sample=sample4)

V11_im = np.zeros([8064,1])
V22_im = np.zeros([8064,1])
V33_im = np.zeros([8064,1])
V44_im = np.zeros([8064,1])
for k in v_q_indicator:
     V11_im[k[0],0] = pi_im1[k[0],0]*Q11[k[1],0]+pi_im1[k[0],1]*Q11[k[2],0]
     V22_im[k[0],0] = pi_im2[k[0],0]*Q22[k[1],0]+pi_im2[k[0],1]*Q22[k[2],0]
     V33_im[k[0],0] = pi_im3[k[0],0]*Q33[k[1],0]+pi_im3[k[0],1]*Q33[k[2],0]
     V44_im[k[0],0] = pi_im4[k[0],0]*Q44[k[1],0]+pi_im4[k[0],1]*Q44[k[2],0]

