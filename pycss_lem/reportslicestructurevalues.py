# import modules
import numpy as np

'''
# Description.
Transform and summarize the  slices structures into an array

# Input(s).
List containing all the slices dictionary type structures (slicesSTRCell). 

# Output(s).
Slices dictionary type structures summarized into an nx7 array which rows are 
each slice data, and columns are 'Abscissa', 'Ordinate', 'Area', 'Width', 
'Height', 'Secant Angle Grads',  and 'Water Height' respectively.
(reportedArray).

n+1x8 array like table, that summarizes the data structures of all slices.
the fields in the first row corresponds to the labels in the table; 
the first column is an index numbering; and other cells are the same 
as 'reportedArray' (reportCell).
 
# Example:
# inputs:
slopeHeight = 12.0; slopeDip = np.array([1, 2.5]); crownDist = 10.0
toeDist = 10.0; wtDepthAtCrown = 0; numSlices = 10; slipRadius = 15
pointAtToeVec = np.array([23, 3.3]); pointAtCrownVec = np.array([2, 15.3])
# Previous functions
boundPointsCordsArray, fromToeOriginRowVec, coordTransMat = materialboundary(\
    slopeHeight, slopeDip, crownDist, toeDist)
surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec, \
    slopeHeight, slopeDip, crownDist, toeDist)
watertableDataCell, wtCoordsArray = defineswatertable(wtDepthAtCrown, \
    surfaceDataCell)
existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
    pointAtCrownVec, slipRadius)
slicesSTRCell = divideslipintoslices(slipArcSTR, surfaceDataCell, \
    watertableDataCell, numSlices, pointAtToeVec, pointAtCrownVec)
# This function
print(reportslicestructurevalues(slicesSTRCell))
---
# reportCell, reportedArray = reportslicestructurevalues(slicesSTRCell)
'''
def reportslicestructurevalues(slicesSTRCell):
    numberSlices = len(slicesSTRCell)
    reportedArray = np.zeros((numberSlices, 11))
    
    temp = list(range(numberSlices))
    for i in temp:
        reportedArray[i,0:2] =slicesSTRCell[i]['midPoint']
        reportedArray[i,2] = slicesSTRCell[i]['area']
        reportedArray[i,3] = slicesSTRCell[i]['width']
        reportedArray[i,4] = slicesSTRCell[i]['midHeight']
        reportedArray[i,5] = slicesSTRCell[i]['inclinationAngleGradAtBottom']
        reportedArray[i,6] = slicesSTRCell[i]['inclinationAngleGradAtTop']
        reportedArray[i,7] = slicesSTRCell[i]['wtMidHeight']
        reportedArray[i,8] = slicesSTRCell[i]['wtMidHeightAboveSlope']
        reportedArray[i,9] = slicesSTRCell[i]['hrzMomentArm']
        reportedArray[i,10] = slicesSTRCell[i]['vrtMomentArm']
       
    indexArray = np.reshape(temp,(len(temp),1))
    namesCell = np.array([['Index', 'Abscissa', 'Ordinate', 'Area', 'Width', \
        'Height', 'Secant Angle Grad at Bottom', 'Angle Grad at Top', \
        'Water Height', 'Water Height Above Slope', 'Horizontal Moment Arm', \
        'Vertical Moment Arm']])
    
    #Create the cell (like array)
    reportedArrayTemp = np.around(reportedArray, decimals=1)
    numericValues = np.concatenate((indexArray, reportedArrayTemp),1)
    reportCell = np.concatenate((namesCell[:], numericValues), 0)

    return reportCell, reportedArray
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
