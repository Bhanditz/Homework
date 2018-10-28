# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 19:40:22 2018

@author: Manasi
"""
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def elba(n0=(31999, 0, 1, 0, 0, 0), nVadd=0, tAdd=None, timeSpan=120, nMax=2000000, nRun=1):
    
    ##Add default values check for input!!!!!!!!!!
    #what are the constants
      
   # Solve the system of ODEs for the continuous-variable deterministic model.
   def continous(n0, nVadd, tAdd, timeSpan):
       def ode_model(n,t):
           h,f,s,i,d,v=n #unpack values of n0 and store them as the following variables
           #the following ODEs below need to solved simultaneously
           dhdt=-k1*h*s-k4*h*v #ODE for healthy people
           dfdt=-k1*f*s
           dsdt=k1*h*s-k2*s-k3*s #ODE for sick people
           didt=k2*s+k4*h*v #ODE for immune people
           dddt=k3*s #ODE for dead people
           dvdt=-k4*h*v #ODE for healthy vaccinated people
           ## FREELOADERS
           return dhdt,dsdt,didt,dddt,dvdt
     
       def Jacob(n,t): #jacobian function is used to solve multiple ODU functions at one time
           h,f,s,i,d,v=n # unpacks all values in vector "n" and stores the numbers as the variables listed (n vector has 6 values in it)
           row1=[-k1*n2-k4*n6,-k1*n1,0,0,k4*n1]
           row2=[k1*n2,k1*n1-k2-k3,0,0,0]
           row3=[k4*n5,k2,0,0,0]
           row4=[0,k3,0,0,0,]
           row5=[k4*n5,0,0,0,-k4*n1] 
           jacobian=np.matrix([row1,row2,row3,row4,row5])
           return Jacob
       
       t=np.linspace(0,timeSpan,timeSpan*30)
       Analysis=integrate.odeint(ode_model,n0,t,Dfun=Jacob)
       H=Analysis[:,0]
       S=Analysis[:,1]
       I=Analysis[:,2]
       D=Analysis[:,3]
       V=Analysis[:,4]
       fig = plt.figure(1) 
       plt.plot(t,H,'r--',label='Healthy')
       plt.plot(t,S)
       plt.plot(t,I)
       plt.plot(t,D)
       plt.plot(t,V)
       return
   return
       
    # n=[n[0],n[2],n[3],n[4],n[5]
    
#       if tAdd>0:
#            tbadd=np.linspace(0,tAdd,tAdd*30)
#            Analysisb=integrate.odeint(ode_model,n0,tbadd,Dfun=Jacob) 
#            Analysisb[-1,4]=Analysisb[-1,4]+vAdd
#            taadd=np.linspace(tAdd,timeSpan,(timeSpan-tAdd)*30)
#            Analysisa=integrate.odeint(ode_model,Analysis[-1,:],taadd,Dfun=Jacob)
#            Analysis=np.concatenate((Analysisa, Analysisb))
#       else: 
#t=np.linspace(0,timeSpan,timeSpan*30)
#Analysis=integrate.odeint(ode_model,n0,t,Dfun=Jacob) 
#    Speople=integrate.odeint(dsdt, n, t, Dfun=Jacob)
#    Ipeople=integrate.odeint(didt, n, t, Dfun=Jacob)
#    Dpeople=integrate.odeint(dddt, n, t, Dfun=Jacob)
##    Vpeople=integrate.odeint(dvdt, n, t, Dfun=Jacob)
#H=Analysis[:,0]
#S=Analysis[:,1]
#I=Analysis[:,2]
#D=Analysis[:,3]
#V=Analysis[:,4]
##    
#fig = plt.figure(1) 
#plt.plot(t,H,'r--',label='Healthy')
#plt.plot(t,S)
#plt.plot(t,I)
#plt.plot(t,D)
#plt.plot(t,V)
  #  return
            

gig=elba(n0=(31999, 0, 1, 0, 0, 0), nVadd=0, tAdd=0, timeSpan=120, nMax=2000000, nRun=1)

        
       
#   return t, n
#
#   def Gillespie_model(…):
# #Apply the Gillespie algorithm for the discrete-variable stochastic model.
#   return t, n
    

    
    