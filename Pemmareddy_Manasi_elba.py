# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:29:40 2018

@author: Manasi
"""
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def elba(n0=(31999, 0, 1, 0, 0, 0), nVadd=0, tAdd=None, timeSpan=120, nMax=2000000, nRun=1):
    """ This function determines how a population will change over time when given, h=healthy ppl, 
    f=freeloading ppl, s=sick ppl, i=immune ppl, d=dead ppl, v=doses of vaccine. Ontop of that
    you can specify the time range (timeSpan) whether or not a certain number of vaccines can 
    be added (nVadd) at a certain time in the timeSpan (tAdd). Using these values, this function
    contains the differenatial equations that can be solved in two ways: continous and discrete 
    model and then they are graphed. nMax and nRun are for discrete model"""
  
    k1=1.76e-5 #rate constants
    k2=0.1
    k3=0.01
    k4=3.52e-6  
    
    #Error handling if input values are not correct
    nVadd=abs(nVadd) #ensures only positive values
    nRun=abs(nRun)
    nMax=abs(nMax)
    
    if nVadd>0 and tAdd==None: #if nVadd>0, then tAdd must be >0, if not, set to default values
        nVadd=0
        tAdd=None
        
    if tAdd != None: #if tAdd DOES NOT equal None
        if tAdd>timeSpan:
            tAdd=None
        elif tAdd<0:
            abs(tAdd)
          
    if nRun==0: #nRun must be greater than or equal to 1, if not, set to default value
        nRun=1
    
    
#CONTINOUS MODEL    
    def ode_model(n,t):
        h,f,s,i,d,v=n #unpack values of n0 and store them as the following variables
               #the following ODEs below need to solved simultaneously
        dhdt=-k1*h*s-k4*h*v #ODE for healthy people
        dfdt=-k1*f*s #ODE for free loaders (needed to derive this on my own)
        dsdt=k1*h*s+k1*f*s-k2*s-k3*s #ODE for sick people
        didt=k2*s+k4*h*v #ODE for immune people
        dddt=k3*s #ODE for dead people
        dvdt=-k4*h*v #ODE for vaccines     
        return dhdt,dfdt,dsdt,didt,dddt,dvdt #need to return these values (can't just say "return")
          
    def Jacob(n,t): #jacobian function is used to solve multiple ODE functions at one time
        h,f,s,i,d,v=n # unpacks all values in vector "n" and stores the numbers as the variables listed (n vector has 6 values in it)
        #jacobian matrix=[ 1st col=dfunction/dh, 2nd col=dfunction/df, 3rd col=dfunction/ds, 4th col=dfunction/di, 5th col=dfunction/dd, 6th col=dfunction/dv]
        row1=[-k1*s-k4*v,0,-k1*h,0,0,-k4*h] 
        row2=[0,-k1*s,-k1*f,0,0,0]
        row3=[k1*s,k1*s,k1*h+k1*f-k2-k3,0,0,0]
        row4=[k4*v,0,k2,0,0,k4*h]
        row5=[0,0,k3,0,0,0,]
        row6=[-k4*v,0,0,0,0,-k4*h]
        jacobian=np.matrix([row1,row2,row3,row4,row5,row6]) #creating matrix
        return jacobian #need to return these values (can't just say "return")
           
    if tAdd!= None: #if tAdd DOES NOT equal None
        tbadd=np.linspace(0,tAdd,tAdd*30) #make time vector that goes from 0 to tAdd
        Analysisb=integrate.odeint(ode_model,n0,tbadd,Dfun=Jacob) # solve the ODE equations for the tbadd time range 
        Analysisb[-1,5]=Analysisb[-1,5]+nVadd #take the last row and and 6th column (vacinne column) and add the additional number of vaccines
          
        taadd=np.linspace(tAdd,timeSpan,(timeSpan-tAdd)*30) #make time vector that goes from tAdd to timeSpan
        Analysisa=integrate.odeint(ode_model,Analysisb[-1,:],taadd,Dfun=Jacob) # solve the ODE equations from the taadd time range
          
        Analysis=np.concatenate((Analysisb, Analysisa)) #combine the two Analysis arrays
        t=np.concatenate((tbadd, taadd)) #combine the the two time range matrices
    else: #if tAdd DOES equal None
        t=np.linspace(0,timeSpan,timeSpan*30)  #don't need to split the time range and combine them in the end
        Analysis=integrate.odeint(ode_model,n0,t, Dfun=Jacob) # solve the ODE equations for the time range t
    
    
    H=Analysis[:,0] #storing the values of the first column (change in healthy peoplutation) as variable H
    F=Analysis[:,1]
    S=Analysis[:,2]
    I=Analysis[:,3]
    D=Analysis[:,4]
    
#DISCRETE MODEL    
    for nR in range(nRun):
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
        
        nonzero = np.logical_not(np.all(dyl==0,axis = 1)) #if in the for loop, the code exits the for loop before hitting nMax,...
                                                          #...then arrays "timey" and "dyl" will still have row of zeros, so this command will identify which rows are non-zero rows       
        timey=timey[nonzero] #restoring the timey and dyl arrays with just the non-zero values
        dyl=dyl[nonzero]
        thom[nR]=dyl[-1,4] #stores the last row of dead column (last row column 4)
    
    
#PLOTTING CONTINOUS AND DISCRETE GRAPHS (don't plot vaccines)  
    #Continous Model 
    plt.subplot(2,1,1)
    plt.title('Continous Model (Top) vs Discrete Model (Bottom)')  
    plt.ylabel('Number of People')
    plt.xlabel('Number of Days')
    plt.plot(t,H,'r--',label='Healthy')
    plt.plot(t,F,'b--', label='Freeloaders')
    plt.plot(t,S,'c--', label='Sick')
    plt.plot(t,I,'g',label='Immune')
    plt.plot(t,D,'k-.',label='Dead')
    plt.legend()

    #Discrete Model  
    if nRun>1:
        plt.subplot(2,1,2)
        plt.ylabel('Frequeny')
        plt.xlabel('Number of Dead People')
        plt.hist(thom,bins=np.arange(np.max(thom)+5)-0.5,edgecolor='black')
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
        
    return #ending elba function
    
    
Juggie=elba()
