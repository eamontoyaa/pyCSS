# import modules
import numpy as np
import matplotlib.pyplot as plt

'''
# Description.
Obtains the coordiantes and also plots the arc that forms the slip
surface, knowing the points at crown and toe, number of slices and
slip arc structure obtained previously with 'defineslipcircle' function. The
segment arc is represented as a polyline, therefore one should give the
number of segments the arc may de divided, but it is recommended to be
equal to the number of slices in future calculations.

# External sub-function(s): none.

# Input(s).
Two dimensional vector of the coordinates that defines the slip at the
slope toe (pointAtToeVec);

Two dimensional vector of the coordinates that defines the slip at the
slope crown (pointAtCrownVec);

Number of polylines that defines the arc (nDivs).

Dictionary type structure of the arc that defines the slip (slipArcSTR). 

Boolean value of true if a plot of the resulting arc is wanted. Default value
is False (want2plot).

# Output(s).
A n x 2 array that represents the coordiantes of the points that defines
the slip arc (arcPointsCoordsArray).

# Example1:
pointAtToeVec = np.array([23, 3.3]); pointAtCrownVec = np.array([2, 15.3])
nDivs = 6; want2plot = True;
slipArcSTR = {'center': np.array([ 31.39356183,  45.39357203]),
  'deepDist': 10.908772031832854,
  'endAngGrad': 284.45218279917071,
  'iniAngGrad': 218.34366020340661,
  'leftDist': -3.0912381712059478,
  'radius': 34.4848}
  
is obtaided:
arcPointsCoordsArray=
    array([[ 23.        ,  11.94585834],
           [ 19.5       ,  13.02468855],
           [ 16.        ,  14.53519091],
           [ 12.5       ,  16.54509283],
           [  9.        ,  19.1689687 ],
           [  5.5       ,  22.6180394 ],
           [  2.        ,  27.35971626]])

---
arcPointsCoordsArray = sliparcdiscretization(pointAtToeVec, \
   pointAtCrownVec, nDivs, slipArcSTR)
'''
def sliparcdiscretization(pointAtToeVec, pointAtCrownVec, nDivs, slipArcSTR,\
     want2plot = False ):

    ## Doing the math
    xCoordIni = pointAtCrownVec[0]
    xCoordEnd = pointAtToeVec[0]
    
    xCoords = np.linspace(xCoordIni, xCoordEnd, nDivs+1)
    yCoords = slipArcSTR['center'][1]-np.sqrt(slipArcSTR['radius']**2\
        -(xCoords-slipArcSTR['center'][0])**2)
    
    arcPointsCoordsArray = np.transpose(np.vstack((xCoords, yCoords)))
    arcPointsCoordsArray = np.flipud(arcPointsCoordsArray)
    
    ## Plotting the arc
    if want2plot:
        # plt.hold(True)
        plt.axis('equal')
        plt.plot(arcPointsCoordsArray[:,0], arcPointsCoordsArray[:,1], 'g-')
        plt.grid(True)
        plt.show(False)

    return arcPointsCoordsArray
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
