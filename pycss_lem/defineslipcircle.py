# Import modules
import numpy as np

from .circleby2ptsradius import circleby2ptsradius
from .unitvector import unitvector
from .azimuthangle import azimuthangle

'''
# Description.
Define the values of the slip circle arc (i.e. arc center point, radius
and initial and final angles ) by giving two extreme points and the circle
radius.

# External subfunction(s):
circleby2ptsradius, azimuthangle, unitvector.

# Input(s).
Two dimensional vector of the coordinates that defines the slip at the
slope toe (pointAtToeVec);

Two dimensional vector of the coordinates that defines the slip at the
slope crown (pointAtCrownVec);

Arc radius (slipRadius).

# Output(s).
Boolean variable giving True if an arc is possible within the given
input variables and the sense of a slip surface (existSlipCircleTrue).
Normaly, any arc can satisfy two points and a radius definition; but there
are less arcs can either attain the conditions to be an concave inferior
arc to represent a slip surface.

Dictionary type structure of the arc that defines the slip (slipArcSTR). 
The fields of the strucrure is as following:
    center: center of the slip arc;
    radius: radius of the slip arc;
    iniAngGrad: counter clockwise angle (in sexagesimal grades)
        from a reference unit vector [1 0] to the initial radius that
        defines the arc;
    endAngGrad: counter clockwise angle (in sexagesimal grades)
        from a reference unit vector [1 0] to the final radius that
        defines the arc;
    deepDist: deepest distance from toe--point horizontal
        reference where the arc passes;
    leftDist: most left distance from toe--point vertical
        reference where the arc passes;

# Example1:
When putting the following inputs:
  pointAtToeVec = np.array([40, 12])
  pointAtCrownVec = np.array([4.347, 24])
  slipRadius = 34.4848
The outputs then are:
  True,
  {'center': array([ 31.39356183,  45.39357203]),
  'deepDist': 10.908772031832854,
  'endAngGrad': 284.45218279917071,
  'iniAngGrad': 218.34366020340661,
  'leftDist': -3.0912381712059478,
  'radius': 34.4848}
---
existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
     pointAtCrownVec, slipRadius)
'''
def defineslipcircle(pointAtToeVec, pointAtCrownVec, slipRadius):

    ## Finding out the two possible centers within the points
    centerVec1, centerVec2 = circleby2ptsradius(pointAtToeVec, \
        pointAtCrownVec, slipRadius)
    
    ## Verifying if exist a circle
    existSlipCircleTrue = True
    error = False
    for i in list(range(len(centerVec1))):
        if centerVec1[i] == 'NaN' or centerVec2[i] == 'NaN':
            existSlipCircleTrue = False
        break
            
    ## Doing the math
    if existSlipCircleTrue == False:
        error = True
        
    else:     
        ## Selecting the appropriate center vector for the slip circle.
        # The line unit vector.
        diffVec = (pointAtCrownVec-pointAtToeVec)
        diffUnitVec = unitvector(diffVec)
        
        # The line equation (analitical eq.).
        lineSlope = diffUnitVec[1]/diffUnitVec[0]
        intercept = pointAtToeVec[1]-lineSlope*pointAtToeVec[0]
        
        # Verifying.
        y1 = intercept+lineSlope*centerVec1[0]
        y2 = intercept+lineSlope*centerVec2[0]
        if centerVec1[1] >= y1 and centerVec2[1] < y2:
            slipCenterVec = centerVec1
        elif centerVec1[1] < y1 and centerVec2[1] >= y2:
            slipCenterVec = centerVec2
        else:
            print ('error: there is no slip at that points')
            error = True

    if error == True:
        ##assigning values
        slipCenterVec = np.array(['NaN', 'NaN'])
        slipRadius = 'NaN'
        initialAngleGrad = 'NaN'
        endAngleGrad = 'NaN'
        deepestVertDepth = 'NaN'
        mostleftHorzDist = 'NaN'
    else:
        ## Finding out the sector initial and final angles.
        # Toe vector.
        toeCenter2PtVec = pointAtToeVec-slipCenterVec
        toeCenter2PtUnitVec = unitvector(toeCenter2PtVec)
        toeRadiusAngleRad = azimuthangle(toeCenter2PtUnitVec)
        endAngleGrad = toeRadiusAngleRad*180/np.pi
        # Crown vector.
        crownCenter2PtVec = pointAtCrownVec-slipCenterVec;
        crownCenter2PtUnitVec = unitvector(crownCenter2PtVec)
        crownRadiusAngleRad = azimuthangle(crownCenter2PtUnitVec)
        initialAngleGrad = crownRadiusAngleRad*180/np.pi
        
        # Extreme slip values.
        # Deepest vertical point at the slip circle
        deepestVertDepth = slipCenterVec[1]-slipRadius
        # Nost Left horizontal distance at the slio circle
        mostleftHorzDist = slipCenterVec[0]-slipRadius
    
    ## Creating the structure    
    slipArcSTR = {'center': slipCenterVec,
                  'radius': slipRadius,
                  'iniAngGrad': initialAngleGrad,
                  'endAngGrad': endAngleGrad,
                  'deepDist': deepestVertDepth,
                  'leftDist': mostleftHorzDist}
                  
    return existSlipCircleTrue, slipArcSTR
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
