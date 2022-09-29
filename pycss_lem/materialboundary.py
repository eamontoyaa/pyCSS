#Import modules
import numpy as np
import matplotlib.pyplot as plt
from .obtainmaxdepthdist import obtainmaxdepthdist

'''
# Description.
Defines and plots the boundary of the material were the slope stability
analysis will be immersed. The analysis will be performed only in slopes
which faces to the right (i.e. slip to the right in a counter clockwise
sense). Also, this function only creates a standard slope: horizontal
surfaces behind the crown and below the foot of the slope. The boundary
is defined therefore by the slope height and the slope inclination and
the two horizontal distances.

# External sub-function(s):
obtainmaxdepthdist.

# Input(s).
Height of the slope (slopeHeight).

Slope dip, given by a bidimensional vector which represents a vertical 
distance and a horizontal distance that not necesary representing the real 
slope distances [horzDist,vertDist], (slopeDip).

Crown horizontal plane distance (crownDist).

Toe horizontal plane distance (toeDist).

Logical value put as 'True' or 'False' if it is wanted to plot. Default 
value is 'False' (want2plot).

# Output(s):
Contour coordinates of the material boundary given in a n x 2 array
(boundPointsCordsArray).

Row vector that specifies this coordinate system origin problem relative
to the slip toe (fromToeOriginRowVec).

Coordinate system transformation matrix of 2x2 size (coordTransMat).
The reference system of points coordinates are the left bottom side.

# Example1: by giving next values
slopeHeight = 12; slopeDip = np.array([1, 2.5]); crownDist = 10.0;\
toeDist = 10.0; it is obtained:
 
boundPointsCordsArray =    |    fromToeOrginRowVec = array([14.8, 3.30])
(array([[  0.  ,   0.  ],  |    
        [ 24.8 ,   0.  ],  |    coordTransMat = array([[1, 0],
        [ 24.8 ,   3.3 ],  |                           [0, 1]])
        [ 14.8 ,   3.3 ],  |
        [ 10.  ,  15.3 ],  |
        [  0.  ,  15.3 ],  |
        [  0.  ,   0.  ]]) |

---
boundPointsCordsArray, fromToeOriginRowVec, coordTransMat = \
   materialboundary(slopeHeight, slopeDip, crownDist, toeDist)
'''
def materialboundary(slopeHeight, slopeDip, crownDist,\
                     toeDist, want2plot = False):
    
    # Obtaining the maximum depth from the toe
    toeDepth = obtainmaxdepthdist(slopeHeight, slopeDip,\
                                  crownDist, toeDist)
    slopeDipGrad = np.degrees(np.arctan(slopeDip[1]/slopeDip[0]))
    
    # Slope vertical projection (horizontal distance)
    slopeDist = slopeHeight/np.tan(np.radians(slopeDipGrad))
    
    # Creating the contour
    boundPointsCordsArray = np.array([
        [0, 0],
        [(crownDist +slopeDist +toeDist), 0],
        [(crownDist +slopeDist +toeDist), toeDepth],
        [(crownDist +slopeDist), toeDepth],
        [crownDist, (toeDepth +slopeHeight)],
        [0, (toeDepth +slopeHeight)],
        [0, 0]])
    
    # Obtaining the vector that directs the origin of the problem coordiante
    # system
    fromToeOriginRowVec = np.array([(crownDist+slopeDist), toeDepth])
    
    #Coordinate system matrix transformation
    coordTransMat = np.transpose(np.array([[1, 0], [0, 1]]))
    
    # Plotting
    if want2plot:
        # plt.hold(True)
        plt.axis('equal')
        plt.plot(boundPointsCordsArray[:,0], boundPointsCordsArray[:,1], '-k')
        plt.plot(boundPointsCordsArray[:,0], boundPointsCordsArray[:,1], 'or')
        plt.grid(True) 
        plt.show(False)
    
    return boundPointsCordsArray, fromToeOriginRowVec, coordTransMat
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
