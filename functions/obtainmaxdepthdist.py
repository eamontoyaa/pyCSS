# import modules
import numpy as np

''' 
# Description.
With the extreme points of the defined slope, this function obtains the
lower possible boundary in where a slip circle can be, i.e. obtains the
maximum depth computed from the slope toe.

# Input(s).
Height of the slope (slopeHeight).

Slope dip, can be given by an angle in gradians, angle in radians, a
horizontal distance value relative to a unitary vertical distance (i.e.
horz:1), or a bidimensional vector which represents a horizontal distance and
a vertical distance that not necessary representing the real slope distances 
[horzDist, vertDist], (slopeDip).

Crown horizontal plane distance (crownDist).

Toe horizontal plane distance (toeDist).

# Output(s):
Vertical distance from the slide--toe to downwards (toeDepth).

# Example1: By giving next values:
slopeHeight = 12; slopeDip = np.array([2.5, 1]); crownDist = 10.0;\
toeDist = 10.0; it is obtained a toeDepth = 14.44.

---
toeDepth = obtainmaxdepthdist(slopeHeight, slopeDip, crownDist, toeDist)
'''
def obtainmaxdepthdist(slopeHeight, slopeDip, crownDist, toeDist):
    
    #Calculation assuming coordinates origin at the slip--toe
    extremeToePointVec = np.array([toeDist, 0])
    
    #slope vertical projection (horizontal distance)
    slopeDist = slopeHeight*slopeDip[0]/slopeDip[1]
    
    extremeCrownPointVec = np.array([-(slopeDist +crownDist), slopeHeight])
    
    #distance between the two extreme points
    differenceVec = extremeToePointVec-extremeCrownPointVec
    distExtrPts = np.sqrt(np.dot(differenceVec, differenceVec))
    maximumCircleRadius = distExtrPts/2*distExtrPts/differenceVec[0]
    
    #the toe depth is the difference between the maximum--circle radius and the
    #slope height
    toeDepth = maximumCircleRadius-slopeHeight
    
    return toeDepth
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
