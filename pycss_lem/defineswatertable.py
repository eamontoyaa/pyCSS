# import modules
import numpy as np
import matplotlib.pyplot as plt
from .create2dsegmentstructure import create2dsegmentstructure

'''
# Description.
Generates a horizontal watertable can be: coincident with the surface slope, 
be below the surface slope, or be above the foot of the slope.

# External subfunction(s):
create2dsegmentstructure.

# Input(s).
Distance from the horizontal surface at the slope crown to the
watertable (wtDepthAtCrown).

List with data of the surface boundatry geometric definition
(surfaceDataCell), in which each element is a dictionary type
line structure. Each line has the following fields:
     iniPtVec: row vector with the initial coordiantes;
     endPtVec: row vector with the final coordiantes;
      unitVec: line unit vector;
       lambda: line length;
        slope: slope of the line;
   azimuthRad: anglular valor of the slope in radians;
    intercept: the value of the line intercept in the coordiante system.
    
Logical value put as 'True' or 'False' if it is wanted to consider the slope 
partially submerged, ie the foot slope is under the watertable 
(toeUnderWatertable).

Logical value put as 'True' or 'False' if it is wanted to plot. Default 
value is 'False' (want2plot). 

# Output(s).
Similar to 'surfaceDataCell', this variable contains data of a plyline
but that represents the water table surface (watertableDataCell). In each
element of the list is a dictionary type line structure with the same 
variables as the strucures of 'surfaceDataCell' (watertableDataCell).

Array of n x 2 with the coordiantes that define the open polygon of the
water table surface (wtCoordsArray).

## Example1:
# inputs
slopeHeight = 12; slopeDip = np.array([1, 2.5]); crownDist = 10.0;
toeDist = 10.0; fromToeOriginRowVec = np.array([-14.8, -3.30]); 
wtDepthAtCrown = 0
# Previous functions
surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec, \
    slopeHeight, slopeDip, crownDist, toeDist)

The first element of the watertableDataCell list is the dictionary as follows:
{'azimuthRad': 0.0,
  'endPtVec': array([-19.6,   8.7]),
  'iniPtVec': array([-29.6,   8.7]),
  'intercept': 8.6999999999999993,
  'lambda': 10.0,
  'slope': 0.0,
  'unitVec': array([ 1.,  0.])}
and watertable coordinates array is:
 array([[-29.6,   8.7],
        [-19.6,   8.7],
        [-14.8,  -3.3],
        [ -4.8,  -3.3]])
---
watertableDataCell, wtCoordsArray = defineswatertable(wtDepthAtCrown, \
    surfaceDataCell, toeUnderWatertable = False, want2plot = False)
'''
def defineswatertable(wtDepthAtCrown, surfaceDataCell, \
        toeUnderWatertable = False, want2plot = False):

    ## Input management
    
    # Ordinate value at crown
    ordinateAtCrown = surfaceDataCell[0]['iniPtVec'][1]
    ordinateAtToe = surfaceDataCell[-1]['iniPtVec'][1]
    ordinateAtCrownWt = ordinateAtCrown-wtDepthAtCrown
        
    ## When negative values of 'wtDepthAtCrown' abort
    if wtDepthAtCrown >= 0 and toeUnderWatertable == False:
   
        # If is equal then the water table surface is coincident with the 
        # terrain surface.
        if ordinateAtCrownWt == ordinateAtCrown:
            watertableDataCell = surfaceDataCell[:]
            numSegments = len(surfaceDataCell)
            wtCoordsArray = np.zeros((numSegments+1, 2))
            for i in list(range(numSegments)):
                wtCoordsArray[i] = surfaceDataCell[i]['iniPtVec']
            wtCoordsArray[-1] = surfaceDataCell[-1]['endPtVec']
        
        # when water table is between the crown surface and the toe surface
        elif ordinateAtCrownWt < ordinateAtCrown and \
            ordinateAtCrownWt > ordinateAtToe:
                        
            # first line paralell to the crown surface
            wtIniPtVec1 = np.array([surfaceDataCell[0]['iniPtVec'][0], \
                (surfaceDataCell[0]['iniPtVec'][1]-wtDepthAtCrown)])
            wtUnitVec1 =surfaceDataCell[0]['unitVec']
            
            # the end point of the segment is the intersection of the two first
            # lines.
            
            # ...the first segment
            point1Vec = wtIniPtVec1
            unitVec1 = wtUnitVec1
            
            point2Vec =surfaceDataCell[1]['iniPtVec']
            unitVec2 =surfaceDataCell[1]['unitVec']
            
            x = (unitVec1[1]/unitVec1[0]*point1Vec[0]-unitVec2[1]/unitVec2[0]\
                *point2Vec[0]-(point1Vec[1]-point2Vec[1]))/(unitVec1[1]/\
                unitVec1[0]-unitVec2[1]/unitVec2[0])
                
            y = point1Vec[1]+unitVec1[1]/unitVec1[0]*(x-point1Vec[0])
            wtEndPtVec1 = np.array([x, y])
            
            # ...the second segment
            wtIniPtVec2 = wtEndPtVec1
            #wtEndPtVec2 =surfaceDataCell{2}.endPtVec;
            
            # ...the third segment
            wtIniPtVec3 = surfaceDataCell[2]['iniPtVec']
            wtEndPtVec3 = surfaceDataCell[2]['endPtVec']
            
            # the matrix of coordinates
            numSegments = len(surfaceDataCell)
            wtCoordsArray = np.zeros((numSegments+1, 2))        
            wtCoordsArray[0] = wtIniPtVec1
            wtCoordsArray[1] = wtIniPtVec2
            wtCoordsArray[2] = wtIniPtVec3
            wtCoordsArray[3] = wtEndPtVec3
        
        # when water table is below the toe surface
        elif ordinateAtCrownWt <= ordinateAtToe:
            
            numSegments = 1
            
            yCord = ordinateAtCrownWt
            
            wtIniPtVec = np.array([surfaceDataCell[0]['iniPtVec'][0], yCord])
            wtEndPtVec = np.array([surfaceDataCell[-1]['endPtVec'][0], yCord])
            
            wtCoordsArray = np.zeros((numSegments+1, 2))
            wtCoordsArray[0] = wtIniPtVec
            wtCoordsArray[1] = wtEndPtVec

        #creating the structure
        watertableDataCell = []
        for i in list(range(numSegments)):
            segmentSTR = create2dsegmentstructure(wtCoordsArray[i], \
                wtCoordsArray[i+1])
            watertableDataCell += [segmentSTR]            
    
    elif wtDepthAtCrown >= 0 and toeUnderWatertable == True:
        
        numSegments = 1
        
        yCord = ordinateAtCrownWt
        
        wtIniPtVec = np.array([surfaceDataCell[0]['iniPtVec'][0], yCord])
        wtEndPtVec = np.array([surfaceDataCell[-1]['endPtVec'][0], yCord])
        
        wtCoordsArray = np.zeros((numSegments+1, 2))
        wtCoordsArray[0] = wtIniPtVec
        wtCoordsArray[1] = wtEndPtVec        
            
        #creating the structure
        watertableDataCell = []
        for i in list(range(numSegments)):
            segmentSTR = create2dsegmentstructure(wtCoordsArray[i], \
                wtCoordsArray[i+1])
            watertableDataCell += [segmentSTR]
         
    else:
        watertableDataCell, wtCoordsArray = np.nan, np.nan
        print('error: Values must be equal or greater than cero!')
               
    ## Ploting
    if want2plot:
        # plt.hold(True)
        plt.axis('equal')
        plt.plot(wtCoordsArray[:,0], wtCoordsArray[:,1], 'b-')
        plt.grid(True) 
        plt.show(False)

    return watertableDataCell, wtCoordsArray
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
