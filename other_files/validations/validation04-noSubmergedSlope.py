'''
# Description.
This is a minimal module in order to perform a circular arc slope stability 
analysis by the limit equilibrium model by Fellenius and Bishop symplified 
methods.
'''

#------------------------------------------------------------------------------
## Add functions directory
import sys
sys.path += ['../functions']

#------------------------------------------------------------------------------
## Modules/Functions import
import numpy as np
import time

from automaticslipcircles import automaticslipcircles
from onlyonecircle import onlyonecircle

#------------------------------------------------------------------------------
## Poject data
projectName = 'Validation-04'
projectAuthor = 'Exneyder A. Montoya Araque'
projectDate = time.strftime("%d/%m/%y")

#------------------------------------------------------------------------------
## Define inputs
# The slope geometry
slopeHeight = [10, 'm']
slopeDip = np.array([2, 1])
crownDist = [5, 'm']
toeDist = [5, 'm']
wantAutomaticToeDepth = False
if wantAutomaticToeDepth == True:
    toeDepth = ['automatic toe Depth']
else:
    toeDepth = [3, 'm']
# The slip arc-circle
wantEvaluateOnlyOneSurface = True
if wantEvaluateOnlyOneSurface == True:
    hztDistPointAtCrownFromCrown = [-2, 'm']
    hztDistPointAtToeFromCrown = [20, 'm']
    slipRadius = [34.95, 'm']
else:
    numCircles = 2000
    radiusIncrement = [2, 'm']
    numberIncrements = 40
    maxFsValueCont = 2
# Watertable
wantWatertable = True
if wantWatertable == True:
    wtDepthAtCrown = [5, 'm']
else: 
    wtDepthAtCrown = ['No watertable']
toeUnderWatertable = False
# Materials properties.
waterUnitWeight = [9.81, 'kN/m3']
materialUnitWeight = [20, 'kN/m3']
frictionAngleGrad = [19.6, 'degrees']
cohesion = [3, 'kPa']

## Advanced inputs
# Want divide the slip surface in constant width slices?
wantConstSliceWidthTrue = True
# Number of discretizations of slip surface.
numSlices = 15
# Number of discretizations of circular arcs.
nDivs = numSlices
# Select the method to calcualte the safety factor ['Flns', 'Bshp' or 'Allm'].
methodString = 'Allm'
# Select the output format image #['.eps', '.jpeg', '.jpg', '.pdf', '.pgf', \
    # '.png', '.ps', '.raw', '.rgba', '.svg', '.svgz', '.tif', '.tiff'].
outputFormatImg = '.svg' 

#------------------------------------------------------------------------------
# Operations for only one slip surface
if wantEvaluateOnlyOneSurface == True:
    msg = onlyonecircle(projectName, projectAuthor, projectDate, slopeHeight, \
        slopeDip, crownDist, toeDist, wantAutomaticToeDepth, toeDepth, \
        hztDistPointAtCrownFromCrown, hztDistPointAtToeFromCrown, \
        slipRadius, wantWatertable, wtDepthAtCrown, toeUnderWatertable, \
        waterUnitWeight, materialUnitWeight, frictionAngleGrad, cohesion, \
        wantConstSliceWidthTrue, numSlices, nDivs, methodString, \
        outputFormatImg)

#------------------------------------------------------------------------------
# Operations for multiple slip surface   
else:
    automaticslipcircles(projectName, projectAuthor, projectDate, slopeHeight,\
        slopeDip, crownDist, toeDist, wantAutomaticToeDepth, toeDepth, \
        numCircles, radiusIncrement, numberIncrements, maxFsValueCont, \
        wantWatertable, wtDepthAtCrown, toeUnderWatertable, waterUnitWeight, \
        materialUnitWeight, frictionAngleGrad, cohesion, \
        wantConstSliceWidthTrue, numSlices, nDivs, methodString, \
        outputFormatImg)
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
