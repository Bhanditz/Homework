# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:43:32 2018

@author: Manasi Pemmareddy

People who helped me: Bryan Hobocienski, Professor Rathman
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import HW_P1P2 as p

##HOMEWORK P1 PART A
def p1(size=None,method='NR',seed=None, returnSeed=False):
        """
        This function is used to create either a range or tuple of 
        random numbers between 0 and 1. The function has four inputs, the shape of 
        array you want, what method to use to generate numbers, a seed value to base 
        the values off of and whether or not the seed will be displayed at the end.
        When you call this function, you can specify any value for size, either Method
        "NR" or "RANDU", any seed number (this will only be an integer) and  a True or 
        False statement for returnSeed. But at the end of the day, you don't have to
        specifiy anything, because there are deafualts set up for each variable. But 
        the function will then yeild a range or tuple of random numbers and/or a seed 
        based on whtehr or not you said True or False for returnSeed
                        
        Manasi Pemmareddy
        Created: 9/18/28
        People who helped me: Bryan Hobocienski, Professor Rathman
        Sources Used: jakevdp.github.io website
            """
 
        #defining a function with four vairables:
        #"size" is the array size you want
        #"method" referes to the LCG algorithm you want to use
        #"seed" refers to the seed to be used in LCG aglorithm
        #"returnSeed" referes to whether or not to return seed value as output
       
        #This for loop is used to determine which constants to use based on what the user said for "method"
        if type(size)==tuple:
            n=np.prod(size)
        elif size==None:
            n=1
        else:
            n=size
 
        if seed==None: #trying to create the most random number of ever if seed is not provided
            time.sleep(0.5) #this code doesn't work for part d becuase it takes way to long
            #gm.time()[5] gives the second of the min
            #gm.time()[4] gives the minute of the hour
            a1=237 
            y1=time.gmtime()[4]
            b1=83
            c1=time.gmtime()[5]
            seed=(a1*y1+b1) % c1
            
        if method=='RANDU':
            a=1664525
            b=1013904223
            c=2**31
        elif method=='NR':
            a=65539 
            b=0
            c=2**31
        else:
            raise Exception('That Method Does Not Exist')
            
    #create a vector of zeros
        y=np.zeros(n)
        y[0]=seed 
    
    #Creating random values based on the value of number before it and storing in vector y
        for i in range(1,n):
            y[i]=(a*y[i-1]+b) % c #(a*y[i-1]+b) is divided by c and the REMAINDER is stored for y(i)
           
        if type(size)==tuple:
            y=np.reshape(y,size) #reshape the size of the array as the dimensions of size
        
    #Allows variables to show up in "Variable Explorer"   
        if returnSeed==True:
            return y/c, seed #y/c normalizes the vector y to values between 0 and 1
        elif returnSeed==False:     
            return y/c
 
##HOMEWORK P1 PART B
##Method='NR'
#nums = p.p1(size=(5000,3),returnSeed=True) #calling function
#X=nums[0][:,0]
#Y=nums[0][:,1]
#Z=nums[0][:,2]
#fig = plt.figure(1)
#ax = plt.axes(projection='3d')
#ax.scatter(X, Y, Z, s=5);
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_zlabel('z') 
#
##Method='RANDU'
#numsR = p.p1(size=(5000,3),method='RANDU',returnSeed=True) #calling function
#XR=numsR[0][:,0]
#YR=numsR[0][:,1]
#ZR=numsR[0][:,2]
#fig = plt.figure(2)
#ax = plt.axes(projection='3d')
#ax.scatter(XR, YR, ZR, s=5);
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_zlabel('z') 
###CITE: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
#            
##HOMEWORK P1 PART C
"""
The graph shows that shows that the randu generator may actually not be as random as expected;
when then the graph is rotatted on the z-axis, you can see that the points are divinded into planes
thus making the points not as random as expected. This is will have negative consequences, because let's
say that an experiementer was trying to generate a bunch of random points to test to randomize their expereiment, 
it will turn out that their experiement was not so randomized becuase the funtion didn't
test random points, thus skewing the results
"""          

##HOMEWORK P1 PART D
#sol=np.zeros(15000) #need to first define a vector
#for i in range(0,15000): #creating a loop to get 1000 seeds and store in vector sheep
#    sol[i]=p.p1(returnSeed=True)[1]#calling function
#    #my seed equation is unfortunately not random enough which is why I keep getting the points
#    #but I have tried so many ways still didin't get a good equation. I spent way too much time on 
#    #time in this, at this point, this is the best answer I have 
#    
#
#sol=np.reshape(sol,(5000,3)) # reshape the array
#X=sol[:,0] #then sstore the columns
#Y=sol[:,1]
#Z=sol[:,2]
#fig = plt.figure()
#ax = plt.axes(projection='3d')
#ax.scatter(X, Y, Z, s=5); #graphing
#ax.set_xlabel('x')
#ax.set_ylabel('y')
#ax.set_zlabel('z')   


##HOMEWORK P2 
def p2(nDraws=200,method='NR'):
    """
    This function is used to create either a range or tuple of 
    random numbers between 0 and 1. The function has two inputs, the shape of 
    array you want, what method to use to generate numbers.
    When you call this function, you can specify any value for nDraws, and either Method
    "NR" or "RANDU". But at the end of the day, you don't have to 
    specifiy anything, because there are deafualts set up for each variable. So the 
    function will actually call function p1 to generate a nDraw by 2 tuple of
    random numbers and then graph them on a graph that has a circle in it. there will be 
    a probabaility of pi value on the graph that shows hoe many points ended up in the cricle
    
    Manasi Pemmareddy
    Created: 9/21/28
    People who helped me: Bryan Hobocienski, 
    Sources Used: www.learningaboutelectronics.com website
       """
    loc=p.p1(size=(nDraws,2)) #recalls function p1 to genarate random numbers
    
    cx=0.5
    cy=0.5
    nsync=0
    
    for i in range(0,nDraws):
        distance=np.sqrt((loc[i,0]-0.5)**2+(loc[i,1]-0.5)**2) #comparing distance bewteen centre of circle to a point in the vector loc
        if distance<=0.5:
            nsync=nsync+1 #doing a running sum to see how much  are within the circle
    
    probability=(nsync/nDraws)*4 #estimating value of pi
    
    #Graphing
    s='estimate of pi:'+str(probability)
    plt.scatter(loc[:,0],loc[:,1])
    circle = plt.Circle((0.5, 0.5), radius=0.5, color='k', linewidth=1, fill=False)
    plt.gca().add_patch(circle)
    plt.title(s)
    plt.axis('scaled')
    plt.show()
    #CITE: http://www.learningaboutelectronics.com/Articles/How-to-draw-a-circle-using-matplotlib-in-Python.php


#keke=p.p2()
        
        
        
        
        
        