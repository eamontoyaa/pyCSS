# import modules
import numpy as np
from .unitvector import unitvector
from .azimuthangle import azimuthangle

'''
tangentlineatcirclept means: 'tangent--line at circle point'

# Description.
Calculates a line that is tangent to a specificed point that belongs to a
circular arc. The code verifies if the point belongs to the circular arc
equation (i.e. the circle), and tolerates some points that could be
closer to the circle by recalculating the y coordianted based on the x
coordinate of the point. If the point belongs to the circle of the arc, it
verfies if that point is betwwen the limits that defines the arc.

# External sub-function(s): unitvector, azimuthangle.

# Input(s).
Two-dimensional vector that defines the point that belongs to the circle
(atCirclePointVec);

Structure of an circular arc from which the circle belongs and at which
the tanget line is wanted to obtain (slipCircleSTR). It's obtained previously
with 'defineslipcircle' function. This structure has the following fields:
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

# Output(s).
Boolean variable with a true value if the given point is inside the
circular arc (isPtBetweenArcLimitsTrue).

Structure of an infinite line (tangentLineSTR). The following fields forms
this structure:
  refPtVec
  unitVec
  slope
  nearestAzimuthAngRad
  farestAzimuthAngRad
  intercept
Among the fields of this structure, some of them are easy to understand;
but the nearesAzimuthAngRad is the angle of the azimuth (given in radians)
of the tangent sense that is nearest to the reference vector [1 0] when
turning couterclockwise sense.
Then the 'farestAzimuthAngRad' is a similar azimuth angle of the oposite
tangent sense.

# Example1:
atCirclePointVec = np.array([16.7036, 14.1941])
slipCircleSTR = {'center':np.array([31.3936, 45.3936]), 'radius':34.4848,
    'iniAngGrad': 218.3437, 'endAngGrad': 284.4522, 'deepDist': 10.9088,
    'leftDist': -3.0912}

---
isPtBetweenArcLimitsTrue, tangentLineSTR = tangentlineatcirclept\
    (atCirclePointVec, slipCircleSTR)
'''
def tangentlineatcirclept(atCirclePointVec, slipCircleSTR):
    
    #Recalculating the point at circle
    distanceTolerance = 0.01*slipCircleSTR['radius']
    
    #Point to cicle--center vector
    ptCenVec = atCirclePointVec-slipCircleSTR['center']
    unitPtCenVec = unitvector(ptCenVec)
    
    #vector length
    vectorLength = np.sqrt(np.dot(ptCenVec, ptCenVec))
    #vector length must be near to the circle radius
    if vectorLength <= slipCircleSTR['radius']+distanceTolerance and \
            vectorLength >= slipCircleSTR['radius']-distanceTolerance:
        #Calculate the new at--circle point
        newAtCirclePtVec = slipCircleSTR['center']+slipCircleSTR['radius']\
            *unitPtCenVec
    else:
        #print ('Error in "tangentlineatcirclept": The given point does not '+
        #'belongs to the circle', sep="")
        newAtCirclePtVec = slipCircleSTR['center']+slipCircleSTR['radius']\
            *unitPtCenVec        
    
    #Tangent line paramemters
    tangentPoint = newAtCirclePtVec
    unitTangentVec = np.array([unitPtCenVec[1], -1*unitPtCenVec[0]])
    if unitTangentVec[0] == 0:
        tangentSlope = np.inf
    else:
        tangentSlope = unitTangentVec[1]/unitTangentVec[0]
    tangentIntercept = tangentPoint[1]-tangentSlope*tangentPoint[0]

    #Verifying if the point is between the arc extremes
    azimuthAngleGrad = azimuthangle(unitPtCenVec)*180/np.pi
    if azimuthAngleGrad >= slipCircleSTR['iniAngGrad']:
        if azimuthAngleGrad <= slipCircleSTR['endAngGrad']:
            isPtBetweenArcLimitsTrue = True
        else:
            isPtBetweenArcLimitsTrue = False
    else:
        isPtBetweenArcLimitsTrue = False

    #calculating nearest and farest azimuth
    angle1Rad = azimuthangle(unitTangentVec)
    angle2Rad = azimuthangle(-1*unitTangentVec)
    if angle1Rad < angle2Rad:
        nearestAzimuthAngRad = angle1Rad
        farestAzimuthAngRad = angle2Rad
    elif angle1Rad > angle2Rad:
        nearestAzimuthAngRad = angle2Rad
        farestAzimuthAngRad = angle1Rad
    elif angle1Rad == angle2Rad:
        nearestAzimuthAngRad = angle1Rad
        farestAzimuthAngRad = angle1Rad
    
    #Building the structure
    tangentLineSTR = {
    'refPtVec': tangentPoint,
    'unitVec': unitTangentVec,
    'slope': tangentSlope,    
    'nearestAzimuthAngRad': nearestAzimuthAngRad,
    'farestAzimuthAngRad': farestAzimuthAngRad,
    'intercept': tangentIntercept}
    
    return isPtBetweenArcLimitsTrue, tangentLineSTR
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
