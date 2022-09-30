# import modules
import numpy as np

'''
# Description:
Get the coordinates of the points defining a polyline 'A', extracted from 
another, and two end points corresponding to the beginning and end of 'A'.

# Input(s):
First point given by a two-dimensional array (pointOneVec);
Second point given by a two-dimensional array (pointTwoVec);
Polyline structure (surfaceDataCell).

# Output(s):
Array nx2 containing the coordinates that belongs to the new polyline
(plineChordsArray).

# Example1:
pointOneVec = np.array([4.3470, 24]); 
pointTwoVec = np.array([12.0085, 23.1966]);
surfaceDataCell = [
   {'iniPtVec':np.array([0, 24]), 'endPtVec':np.array([10, 24]), 'unitVec':\
   np.array([1, 0]), 'lambda':10, 'slope':0, 'azimuthRad':0, 'intercept':24},
   {'iniPtVec':np.array([10, 24]), 'endPtVec':np.array([40, 12]), 'unitVec':\
   np.array([0.9285, -0.3714]), 'lambda':32.3110, 'slope':-0.4228, 
   'azimuthRad':5.9027, 'intercept':34.1470},
   {'iniPtVec':np.array([40, 12]), 'endPtVec':np.array([50, 12]), 'unitVec':\
    np.array([1, 0]), 'lambda':10, 'slope':0, 'azimuthRad':0, 'intercept':12}]

it's obtained:
   plineChordsArray = 
      array([[ 12.0085   ,  29.0698062],
             [ 10.       ,  24.       ],
             [  4.347    ,  24.       ]])
---
plineChordsArray = extractplinefrom2pts(pointOneVec, pointTwoVec, \
    surfaceDataCell)
'''
def extractplinefrom2pts(pointOneVec, pointTwoVec, surfaceDataCell):
    
    if pointTwoVec[0] < pointOneVec[0]:
        temp = pointOneVec
        pointOneVec = pointTwoVec
        pointTwoVec = temp
        
    ## Number of lines.
    numLines = len(surfaceDataCell)
    
    ## For the first point.
    firstPtBelongArray = np.zeros(numLines)
    for i in list(range(numLines)):
        if pointOneVec[0] >= surfaceDataCell[i]['iniPtVec'][0] and \
            pointOneVec[0] < surfaceDataCell[i]['endPtVec'][0]:
            firstPtBelongArray[i] = 1
            break

    pointOnePlineIndex = np.nonzero(firstPtBelongArray)[0]

    ## For the second point.
    secondPtBelongArray = np.zeros(numLines)
    for i in list(range(numLines)):
        if pointTwoVec[0] >= surfaceDataCell[i]['iniPtVec'][0] and \
            pointTwoVec[0] < surfaceDataCell[i]['endPtVec'][0]:
            secondPtBelongArray[i] = 1
            break

    pointTwoPlineIndex = np.nonzero(secondPtBelongArray)[0]

    ## Now it will built the array, but with extremes values.
    numSubPoints = (sum(pointTwoPlineIndex)-sum(pointOnePlineIndex)+1)*2
    plineChordsArray = np.zeros((numSubPoints, 2))
    j = 0
    for i in list(range(sum(pointOnePlineIndex), sum(pointTwoPlineIndex)+1)):
        tempo1Array = surfaceDataCell[i]['iniPtVec']
        tempo2Array = surfaceDataCell[i]['endPtVec']
        plineChordsArray[j:j+2,:] = np.array([tempo1Array, tempo2Array])
        j += 2

    ## Now one will replace the extreme values.
    # Left end.
    xLeftEnd = pointOneVec[0]
    yLeftEnd = surfaceDataCell[pointOnePlineIndex[0]]['intercept']\
        +surfaceDataCell[pointOnePlineIndex[0]]['slope']*pointOneVec[0]
    # Right end.
    xRightEnd = pointTwoVec[0]
    yRightEnd = surfaceDataCell[sum(pointTwoPlineIndex)]['intercept']\
        +surfaceDataCell[sum(pointTwoPlineIndex)]['slope']*pointTwoVec[0]
    
    plineChordsArray[0,:] = np.array([xLeftEnd, yLeftEnd])
    plineChordsArray[-1,:] = np.array([xRightEnd, yRightEnd])
    
    ## Extracting unique values.
    plineChordsArray = np.vstack(list({tuple(row) for row in plineChordsArray}))
    ## Sorting the array (key=item[0]) upwardly.
    plineChordsArray = plineChordsArray[plineChordsArray[:,0].argsort()]
    ## Arranging inverse.
    plineChordsArray = np.flipud(plineChordsArray)

    return plineChordsArray

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
