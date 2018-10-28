# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 10:28:43 2018

@author: Manasi
"""


import numpy as np #import numpy package
import matplotlib.pyplot as plt #importmatplotlib.pyplot package for creating.. 
                                #...plots and graphical visualizations

n0=(200,0,0,0,0,0) #creating a tuple-ordered collections of other objects-of...
                  #... the number of the various Rn isotopes at time zero"
thalf=np.array((3.8235*24,3.10/60,26.8/60,19.9/60,
                (164.3e-6)/3600,22.2*365*24)) #creates an array of the...
                #...half-life of  corresponding isotopes in the n0 tuple in hrs
tau=thalf/np.log(2) #calulates the mean life time of the halflives

dt=0.1
tmax=500.
t=np.arange(0.,tmax,dt) #creating a time array, starting at 0, ending at...
                         #...tmax-dt, with a step size of dt
p=np.exp(-dt/tau) #computing the fraction 1/m of radioactive atoms expected to...
                #...survive during any general time interval t1/m 
                #a.k.a the probability of not decaying
n=np.zeros((t.size,6),dtype=np.int) #create an array of zeroes
#... with the # of rowss equiv to lenght of t and 6 columns for 6 isotopes
n[0,:]=n0 # Replaces first row in n matrix with values in n0

for i in range(1,t.size): #the number of loops equals length of array t
    n[i,:]=np.random.binomial(n[i-1,:],p)
#the takes the row before the current index number (n[i-1]) and finds the...
#... probability of the number of atoms NOT decaying for each isotope and...
#... stores those values in the current row index
    d=n[i-1,:]-n[i,:] #subtracts previous row from the current row to find..
    #...the number of atoms that decay to the NEXT ISOTOPES & yeilds an array
    n[i,1:]=n[i,1:]+d[:-1] #Then that array is placed into the columns 1-5...
    #..of the the current vector to show how many of each isotopes there are
    #d[:-1] means that all columns except the last column since that doesn't..
    #..decay into anything
    
lines=plt.step(t,n) #plotting t and n arrays (n is a matrix that has 6...
#..columns -  so graph will yeild 6 lines: t vs every column in matrix -...
#...since each column is an isotype
plt.title('CBE 5790, Homework P0') #labeling the the x and y axis and title
plt.xlabel('time(hr)')
plt.ylabel('number')
plt.legend(('$^{222}$Rn','$^{218}$Po','$^{214}$Pb','$^{214}$Bi','$^{214}$Po',
            '$^{210}$Pb'), loc='best')