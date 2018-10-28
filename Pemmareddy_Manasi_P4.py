# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:25:48 2018

@author: Manasi

People who helped me: Edward (TA)
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import time

#function call definition
def pendulum(thetaZero=30, damp=0, timeSpan=20, length=0.45, gravity=0.8):
    """"
    This function allows the user to input, initial angle displacement, damping 
    coefficeint, time span of simulation, lenght of pendulum, and gravity.
    From there, the function will caluclate a set of pendulum motion data (meters)  
    based on a real equation (based on jacobian) and a simple equation. Then that
    data is plotted onto a graph and the motion is set up to run for a period 
    of time(timeSpan) """
    
    thetaZero=np.deg2rad(thetaZero)
    
    ## These abs() commands makes sures that the variables are positive incase a negative value was put in
    damp=abs(damp)
    timeSpan=abs(timeSpan)
    length=abs(length)
    gravity=abs(gravity)
    
    ## Real function: the ODE (Eq 3 from porblem statement)
    def dwdt(w,t):
        #this dw equations is the dw/dt equation 3 from problem statement
        #the first term is the w(0) initialized value and then the second term is the actual equation 
             dw=[w[1], -damp*w[1]-gravity*(np.sin(w[0])/length)] 
             return dw
         
    #Jacobian definition: helps fine tune the dadt function
    def jacobian(w,t):
             w1,w2=w # unpacks w and stores the values as w1 and w2
             dada1=[0,1]
             dada2=[((-gravity/length)*np.cos(w1)),-damp]
             jacobian=np.matrix([dada1,dada2])
             return jacobian
         
            
    theta0=[thetaZero,0]
    t=np.linspace(0, timeSpan,timeSpan*20) #timeSpan*20 equally spaced terms between 0 and timeSpan
    theta=integrate.odeint(dwdt, theta0, t, Dfun=jacobian) #theta0=w;integrate the oscillation ODE 
    x=length*np.sin(theta[:,0]) #distance from pivot: converting theta to length in meters
    y=-length*np.cos(theta[:,0])
    
    ## Simplified Ocillation Equation (Equation 2 from problem statement)
    t1=np.linspace(0, timeSpan, timeSpan*20) #set the time span for the simple data
    THETA=thetaZero*np.cos(np.sqrt(gravity/length)*t1) #equation 2 from porblem statement
    x1=length*np.sin(THETA) #distance from pivot: converting theta to length in meters
    y1=-length*np.cos(THETA)
    
    ## Creating the Plots  
    ax=plt.axes(xlim=(-1.25*length, 1.25*length), ylim = (-1.25*length,1.25*length)) #defining axis of plots
    
   
    pivot, = plt.plot(0,0) #setting the pivot as point (0,0)
    plt.hold(True)
    point,=plt.plot([],[],'r--', marker='o') #creating empty plot for real data
    point2,=plt.plot([],[],'b--', marker='o')  #creating empty plot for simple data
    #comma unpacks tuple
    
    #labeling the the x and y axis and title
    plt.title('Simple Harmonic Oscillator vs Actual Pendulum Motion') 
    plt.xlabel('horizontal position (m)')
    plt.ylabel('vertical position (m)')
    plt.legend(('real','simple'),loc='best')
    
    
    
    start=time.time() #I start the timer right before animation
   
    #animation setup
    for xpoint,ypoint,x1point,y1point in zip(x,y,x1,y1): #two lists(x,y & x1,y1) and makes as iterator that combines elements and returns an iterator of tuples??
                point.set_data([0,xpoint],[0,ypoint]) #plotting real data into empty plot point,
                point2.set_data([0,x1point],[0,y1point]) #plotting sample data into empty plot point2,
                plt.pause(0.02) #there is a 0.02 second pause between each movement
                if time.time()-start >= timeSpan: break # if the animation exceeds timeSpan seconds, exit for loop
    return 
    
    return

pendulum(thetaZero=30, damp=0, timeSpan=20, length=0.45, gravity=0.8) #calling function