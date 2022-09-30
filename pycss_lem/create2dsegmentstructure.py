# import modules
import numpy as np
from .azimuthangle import azimuthangle
from .unitvector import unitvector

'''
# Description.
Creates a two-dimensional line segment structure from their initial and
final points. It returns a dictionary type segment structure.

# External sub-function(s):
azimuthangle, unitvector.

# Input(s):
Array type two-dimensional vector, that represents the segment initial point
relative to a coordinate system (iniPnt2dRowVec);

Array type two-dimensional vector, that represents the segment end point 
relative to a coordinate system (endPnt2dRowVec); 

# Output(s):
Dictionary type segment structure (segmentSTR) with the following fields:
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

# Example1.
These two points defines a two dimensional segment
  iniPnt2dRowVec = np.array([53.8973, 43.2314])
  endPnt2dRowVec = np.array([69.0489, 50.5464])
the the segment values are as following:
      iniPtVec: [53.8973 43.2314]
       endPtVec: [69.0489 50.5464]
        unitVec: [0.9005 0.4348]
         lambda: 16.8250
          slope: 0.4828
     azimuthRad: 0.4498
      intercept: 17.2105

---
 segmentSTR = create2dsegmentstructure(iniPnt2dRowVec, endPnt2dRowVec)
'''
def create2dsegmentstructure(iniPnt2dRowVec, endPnt2dRowVec):
    
    # Obtaining the unit vector of the segment
    segmentVec = endPnt2dRowVec-iniPnt2dRowVec
    unitVec = unitvector(segmentVec)
    
    # Obtaining the segment length, lambda; 
    # the line equation can be expressed by:
    # $\vec{p}=\vec{p_{\mathrm{o}}} +\lambda \vec{u}$
    lamda = np.sqrt(np.dot(segmentVec, segmentVec))
    
    # Obtaining the segment inclination and sense, based on a 
    # counter-clockwise angle increment from a left--right sense.
    azimuthRad = azimuthangle(unitVec)
    slope = unitVec[1]/unitVec[0]

    # Obtaining the line intercept
    intercept = iniPnt2dRowVec[1]-slope*iniPnt2dRowVec[0]

    # Arranging the structure
    segmentSTR = {
        'iniPtVec': iniPnt2dRowVec,
        'endPtVec': endPnt2dRowVec,
        'unitVec': unitVec,
        'lambda': lamda,
        'slope': slope,
        'azimuthRad': azimuthRad,
        'intercept': intercept}
    
    return segmentSTR
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
