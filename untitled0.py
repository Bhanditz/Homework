# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 05:59:04 2018

@author: Manasi
"""
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def disc(n0=(31999,0,1, 0, 0, 0), nVadd=0, tAdd=None, timeSpan=120, nMax=2000000, nRun=1):
    k1=1.76e-5
    k2=0.1
    k3=0.01
    k4=3.52e-6 
    
    for nR in range(1,nRun):
        timey=np.zeros((nMax,1)) #defining a time vector with nMax rows and and 1 column with zeros
        dyl=np.zeros((nMax,6)) #defining an array of zeros with nMax rows and 6 columns
        dyl[0,:]=n0 #initialize the first row of dyl array with the intial values of n0
        thom=np.zeros((nRun)) # This command is only used for if nRun>1
        h,f,s,i,d,v=n0 #setting up vectors to figure out how much to subtract each value by in each reation
        changes = np.array([[-1,0,1,0,0,0],[0,-1,1,0,0,0],[0,0,-1,1,0,0],[0,0,-1,0,1,0],[-1,0,0,1,0,-1]])
        # the "changes" array shows how the different variables change for each reaction:
            # 1st row refers to rxn: h+s->2s
            # 2nd row refers to rxn: f+s->2s
            # 3rd row refers to rxn:   s->i
            # 4th row refers to rxn:   i->d
            # 5th row refers to rxn: h+v->i
        
            # 1st col=net change in h 
            # 2nd col=net change in f 
            # 3rd col=net change in s 
            # 4th col=net change in i  
            # 5th col=net change in d 
            # 6th col=net change in v
        
        for jj in range(1,nMax):
            r=np.array([k1*h*s,k1*f*s,k2*s,k3*s,k4*h*v]) # rxn rates for rxns 1-5
            rtotal=sum(r) 
            if rtotal==0:
                jj=jj-1 #this is to make sure that this loop doesn't get counted in the matrix
                break
            p=r/rtotal #first reaction rate divided by total reaction rate to determine the probability of each rxn happening
            csp=np.cumsum(p) # finds cummalative sum for each row in the array 
                    
            spr=np.random.uniform(0,1) #pick a random number between 0 and 1 
            cole=np.where(spr<csp)[0][0] #compares the spr value to the values in csp array; then refers to rows in which spr<csp, then refers to the FIRST value if there are multiple rows 
            tou=-np.log(spr)/rtotal #calculating time step change
            if timey[jj-1]+tou>timeSpan: #to ensure the the time value doesn't exceed timeSpan
                jj=jj-1 #this is to make sure that this loop doesn't get counted in the matrix
                break
                
            if tAdd!= None and timey[jj-1]+tou>tAdd:
                timey[jj]=tAdd
                changes[cole,5]=changes[cole,5]+nVadd #at time tAdd, add in the vaccines
                tAdd=None #change to tAdd=None since it only gets added in once
            else:
                timey[jj]=timey[jj-1]+tou #if not, continue to keep adding tou
               
            dyl[jj,:]=dyl[jj-1,:]+changes[cole,:] #the current row equals the previous row plus the net changes in row "cole"
            h,f,s,i,d,v=dyl[jj,:] #unpack the current values of row and restore them as these variables to calculate  r values in the next loop
        
        #thom[nR]=dyl[jj,4]
        nonzero = np.logical_not(np.all(dyl==0,axis = 1)) #if in the for loop, the code exits the for loop before hitting nMax,...
                                                          #...then arrays "timey" and "dyl" will still have row of zeros, so this command will identify which rows are non-zero rows       
        timey=timey[nonzero] #restoring the timey and dyl arrays with just the non-zero values
        dyl=dyl[nonzero]
        thom[nR]=dyl[-1,4]
        
        if nRun>1:
            #fig, ax = plt.subplots(2,1,2)
            plt.subplot(2,1,2)
            #Max_Val=max(thom)
            #bins = np.arange(Max_Val+1) - 0.5
            plt.ylabel('Frequeny')
            plt.xlabel('Number of Dead People')
            plt.hist(thom,bins=np.arange(np.max(thom)+5)-0.5,edgecolor='black')
           # ax.set_xticks(bins[:-10])
            #plt.xticks(range(Max_Val))
            #plt.xlim([-1,max(thom)+1000])
            plt.show()
        else:
            plt.subplot(2,1,2)
            plt.ylabel('Number of People')
            plt.xlabel('Number of Days')
            plt.plot(timey,dyl[:,0],'r--',label='Healthy')
            plt.plot(timey,dyl[:,1],'b--', label='Freeloaders')
            plt.plot(timey,dyl[:,2],'c--', label='Sick')
            plt.plot(timey,dyl[:,3],'g',label='Immune')
            plt.plot(timey,dyl[:,4],'k-.',label='Dead')
            plt.legend()
        
        return thom

juggie=disc(nRun=2)
print(juggie) 


#jug=disc(nVadd=800, tAdd=10)