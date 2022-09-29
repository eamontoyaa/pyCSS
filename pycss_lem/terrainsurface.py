#Import modules
import numpy as np
import matplotlib.pyplot as plt
from .create2dsegmentstructure import create2dsegmentstructure

'''
# Description.
Defines and plots the slope surface tarrain as an open polygon. The
polygon is stored on a list, in which each element is a dictionary type
line structure.

# External sub-function(s):
create2dsegmentstructure.

# Input(s).
Vector that connects the toe with global coordinate system origin
(fromToeOriginRowVec). Obtained with materialboundary function.

Height of the slope (slopeHeight)

Slope dip, given by a 1x2 vector which represents a horizontal distance and
a vertical distance not necesary representing the real slope distances
[horzDist, vertDist], (slopeDip).

Crown horizontal distance (crownDist).

Toe horizontal distance (toeDist).

Logical value put as 'True' or 'False' if it is wanted to plot. Default 
value is 'False' (want2plot).

# Output(s).
One list that stores all the lines conforming the surface
polyline (surfaceDataCell), in which each element is a dictionary type
line structure. Each line has the following fields:
      iniPtVec: vector of the coordinates of the first line point;
      endPtVec: vector of the coordinates of the second line point;
      unitVec: unit vector that defines a direction;
      lambda: value that defines the segment length;
      slope: value that defines the slope of the line equation of the
             segment; 
      azimuthRad: counter-clockwise angle (in radians) from a reference
              axis of [1, 0] to [0, 1];
      intercept: value that defines the intercept of line equation of the 
              segment.

Coordinates of the slope terrain polyline given in a nx2 array
(surfaceChordsArray).

# Example:
By putting the following input variables obtained with materialboundary 
function:

slopeHeight = 12; slopeDip = np.array([1, 2.5]); crownDist = 10.0;\
toeDist = 10.0; fromToeOriginRowVec = np.array([-14.8, -3.30])
 
The first element of the surfaceDataCell list is the dictionary as follows:
{'azimuthRad': 0.0,
  'endPtVec': array([-19.6,   8.7]),
  'iniPtVec': array([-29.6,   8.7]),
  'intercept': 8.6999999999999993,
  'lambda': 10.0,
  'slope': 0.0,
  'unitVec': array([ 1.,  0.])}

---
surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec, 
   slopeHeight, slopeDip, crownDist, toeDist)
'''
def terrainsurface(fromToeOriginRowVec, slopeHeight, slopeDip, crownDist, 
                   toeDist , want2plot = False):
    
    # Slope vertical projection (horizontal distance)
    slopeDist = slopeHeight*slopeDip[0]/slopeDip[1];

    # Creating the temporal surface line coordiantes array
    relSurfaceChordsArray = np.array([
        [-(crownDist +slopeDist), slopeHeight],
        [-slopeDist, slopeHeight],
        [0, 0],
        [toeDist, 0]])
    
    # Creating the absolute coordinate system relative to toe
    tempo01 = fromToeOriginRowVec[0]+relSurfaceChordsArray[:,0]
    tempo02 = fromToeOriginRowVec[1]+relSurfaceChordsArray[:,1]
    surfaceChordsArray = np.transpose(np.vstack((tempo01, tempo02)))
    
    # Creating the data array of dictionary structures:
    numOfPoints = len(surfaceChordsArray[:,0])
    
    surfaceDataCell = []
    for i in list(range(numOfPoints-1)):
        iniPnt2dRowVec = surfaceChordsArray[i,:]
        endPnt2dRowVec = surfaceChordsArray[i+1,:]
        lineSTR = create2dsegmentstructure(iniPnt2dRowVec, endPnt2dRowVec)
        surfaceDataCell += [lineSTR]
        
    # Plotting
    if want2plot:
        # plt.hold(True)
        plt.axis('equal')        
        plt.plot(surfaceChordsArray[:,0], surfaceChordsArray[:,1], 'r--', \
            linewidth=1.5)
        plt.grid(True) 
        plt.show(False)

    return surfaceDataCell, surfaceChordsArray
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
