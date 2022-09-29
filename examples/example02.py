'''
# Description.
This is a minimal module in order to perform a circular arc slope stability 
analysis for the example number 02. #
'''

#-----------------------------------------------------------------------------#
## Modules/Functions import
import numpy as np
import time

from pycss_lem import get_fos

#-----------------------------------------------------------------------------#
### Poject data ###
projectName = 'Example-02'
projectAuthor = 'Exneyder A. Montoya Araque'
projectDate = time.strftime("%d/%m/%y")

#-----------------------------------------------------------------------------#
### Previous  calculations ###
waterUnitWeight = [9.8, 'kN/m3']
materialDryUnitWeight = [13, 'kN/m3']
specificGravity = 2.4
moisture = 0.18
voidRatio = (waterUnitWeight[0]*specificGravity/materialDryUnitWeight[0])-1
materialUnitWeight = [specificGravity*(1+moisture)*waterUnitWeight[0]/\
    (1+voidRatio), 'kN/m3']
materialSatUnitWeight = [(specificGravity+voidRatio)*waterUnitWeight[0]/\
    (1+voidRatio), 'kN/m3']

### Define inputs ###
# The slope geometry #
slopeHeight = [11.5, 'm']
slopeDip = np.array([3, 8])
crownDist = [15, 'm']
toeDist = [15, 'm']
wantAutomaticToeDepth = True
toeDepth = ['automatic toe Depth']
# The slip arc-circle #
hztDistPointAtCrownFromCrown = [-11, 'm']
hztDistPointAtToeFromCrown = [13.5, 'm']
slipRadius = [15.6, 'm']
# Water table depth #
wantWatertable = True
wtDepthAtCrown = [3.7, 'm']
toeUnderWatertable = False
# Materials properties #
waterUnitWeight = waterUnitWeight[:]
materialUnitWeight = materialSatUnitWeight[:]
frictionAngleGrad = [21, 'degrees']
cohesion = [4.5, 'kPa']

### Advanced inputs ###
# Want divide the slip surface in constant width slices? #
wantConstSliceWidthTrue = True
# Number of discretizations of slip surface. #
numSlices = 10
# Number of discretizations of circular arcs. #
nDivs = numSlices
# Select the method to calcualte the safety factor ['Flns', 'Bshp' or 'Allm'] #
methodString = 'Bshp'
# Select the output format image ['.eps', '.jpeg', '.jpg', '.pdf', '.pgf', \ #
    # '.png', '.ps', '.raw', '.rgba', '.svg', '.svgz', '.tif', '.tiff']. #
outputFormatImg = '.svg' 

#-----------------------------------------------------------------------------#
# Operations for only one slip surface #
msg = get_fos(
    projectName,
    projectAuthor,
    projectDate,
    slopeHeight,
    slopeDip,
    crownDist,
    toeDist,
    wantAutomaticToeDepth,
    toeDepth,
    hztDistPointAtCrownFromCrown,
    hztDistPointAtToeFromCrown,
    slipRadius,
    wantWatertable,
    wtDepthAtCrown,
    toeUnderWatertable,
    waterUnitWeight,
    materialUnitWeight,
    frictionAngleGrad,
    cohesion,
    wantConstSliceWidthTrue,
    numSlices,
    nDivs,
    methodString,
    outputFormatImg
)

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
