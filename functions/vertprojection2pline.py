# import modules
import numpy as np

'''
# Description.
Obtains the coordinates of a point ---or a group of points--- projected
vertically to an open polyline.

# Input(s):
Vector of the point is wanted to project vertically to the pline
(pointVec).

Polyline structure cell which has as number of elements as number of
lines it has (plineStructureCell).

# Output(s).
Vector of the projected point (projectedPointVec).

# Example1.
pointVec = np.array([7.35, 18])
plineStructureCell = [
   {'iniPtVec':np.array([0, 24]), 'endPtVec':np.array([10, 24]), 'unitVec':\
   np.array([1, 0]), 'lambda':10, 'slope':0, 'azimuthRad':0, 'intercept':24},
   {'iniPtVec':np.array([10, 24]), 'endPtVec':np.array([40, 12]), 'unitVec':\
   np.array([0.9285, -0.3714]), 'lambda':32.3110, 'slope':-0.4228, 
   'azimuthRad':5.9027, 'intercept':34.1470},
   {'iniPtVec':np.array([40, 12]), 'endPtVec':np.array([50, 12]), 'unitVec':\
   np.array([1, 0]), 'lambda':10, 'slope':0, 'azimuthRad':0, 'intercept':12}]
Giving the answer of:
projectedPointVec = np.array([7.35, 24])

#################
# projectedPointVec = vertprojection2pline(pointVec, plineStructureCell)
'''
def vertprojection2pline(pointVec, plineStructureCell):
    
    projectedPointVec = np.zeros(2)
    numberPlines = len(plineStructureCell)
    
    projectedPointVec[0] = pointVec[0]
    
    for i in list(range(numberPlines)):
        #The line structure
        lineSTR = plineStructureCell[i]
        #Select the proper pline
        if pointVec[0] >= lineSTR['iniPtVec'][0]:
            if pointVec[0] < lineSTR['endPtVec'][0]:
                #Obtaining the y--coordiante at the projected point
                projectedPointVec[1] = lineSTR['intercept']+lineSTR['slope']*\
                    pointVec[0]
                #Finishing the loop
                break
        else:
            projectedPointVec[:] = np.nan
    return projectedPointVec
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
