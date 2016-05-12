## Import modules
import numpy as np
import scipy.linalg as la

'''
Description.
Function used to compute the center of the circle given two points and a
radius. Takes only real inputs and gives only real outputs.
Function originally named: circ_cent.m for MatLab(R)
By: Chiran 2010, BST license

# Input(s):
First circle point (pt1Vec).

Second circle point (pt2Vec).

Circle radius (radius).

# Output(s):
Row vector of the point where the first possible center (centerVec1);

Row vector of the point where the second possible center (centerVec2).

# Example1:
pt1Vec = np.array([40, 12]); pt2Vec = np.array([4.347, 24]); radius = 34.4848
One of the solutions is: np.array([31.3936, 45.3936]).

---
centerVec1, centerVec2 = circleby2ptsradius(pt1Vec, pt2Vec, radius)
'''
def circleby2ptsradius(pt1Vec, pt2Vec, radius):
    
    if radius < la.norm(pt1Vec-pt2Vec)/2:
        centerVec1 = np.array(['NaN', 'NaN'])
        centerVec2 = np.array(['NaN', 'NaN'])
    else:
        a = pt1Vec[0]**2-pt2Vec[0]**2
        b = pt1Vec[1]**2-pt2Vec[1]**2
        c = -2*(pt1Vec[0]-pt2Vec[0])
        d = -2*(pt1Vec[1]-pt2Vec[1])
        e = a+b
        Coeff1 = 1+(d/c)**2
        Coeff2 = ((2*d*e/c**2) +(pt2Vec[0]*2*d/c) -2*pt2Vec[1])
        Coeff3 = ((e/c)**2+(2*pt2Vec[0]*e/c)+pt2Vec[0]**2+pt2Vec[1]**2-\
            radius**2)
        
        All_coeff = np.array([Coeff1, Coeff2, Coeff3])
        Eq_root = np.roots(All_coeff)
        
        # centersArray--center of the circle. It is a 2x2 matrix. First row
        # represents first possible center (x1, y1) and second row is the 
        # second possible center.
        centersArray = np.zeros((len(Eq_root),2))
        
        for i in list(range(len(Eq_root))):
            x = -(e+d*Eq_root[i])/c
            centersArray[i,0] = x
            centersArray[i,1] = Eq_root[i]
        
        # Check if values in centerArray are real or unreal numbers
        if la.norm(centersArray.imag) != 0:
            print('Circle with the specified radius does not pass through',
                'specified points', sep=" ")
            centerVec1 = np.array(['NaN', 'NaN'])
            centerVec2 = np.array(['NaN', 'NaN'])
        else:
            centerVec1 = centersArray[0, :]
            centerVec2 = centersArray[1, :]
        
    return centerVec1, centerVec2
'''
BSD 2 license.

Copyright (c) 2016, Universidad Nacional de Colombia, Ludger O.
   Suarez-Burgoa and Exneyder Andrés Montoya Araque.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:  

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer. 

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.  

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
