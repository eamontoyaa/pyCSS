# import modules
import numpy as np
from .reportslicestructurevalues import reportslicestructurevalues

'''
# Description.
Obtains the safety factor under the Fellenius method for any freatic level
below the slope terrain surface.

# External sub-function(s):
reportslicestructurevalues.

# Input(s).
Cell which in each element has a slice strucure (slicesSTRCell). The
slice structure is as follows:
    plineCords: contains all the coordiantes that gives the
      slice closed polyline;
    area: slice polygon area;
    midPoint: coordinates of the middle point of the slice at its base;
    midHeight: value of the mean height taken the initial,
      middle and end heights of the slice at its base to terrain surface;
    width: value of width slice;
    inclinationAngleGradAtBottom: angle in sexagesimal grades of the
      secant line that passess trough the extreme borders of the bottom slice;
    inclinationAngleGradAtTop: angle in sexagesimal grades of the
      secant line that passess trough the extreme borders of the top slice;
    wtMidHeight: value of the mean height taken the initial,
      middle and end heights of the slice at its base to watertable surface;
    wtMidHeightAboveSlope: value of the mean height taken the initial,
      middle and end heights of the water column above slope surface;
    hrzMomentArm: value of the horizontal component of the moment arm acting 
      on the slope due to the water above it;
    vrtMomentArm: value of the vertical component of the moment arm acting 
      on the slope due to the water above it;

Unit weight of the water (waterUnitWeight).

Geomaterial unit weight in dry state (materialUnitWeight).

Angle of friction of the geomaterial at the slice base (frictionAngleGrad).
 
Cohesion of the geomaterial at the slice base (cohesion).

Value of slip circle radius (slipRadius)

# Output(s).
The safety factor value (sf).

### Example1.
# inputs:
slopeHeight = 12.0; slopeDip = np.array([1, 2.5]); crownDist = 10.0;
toeDist = 10.0; wtDepthAtCrown = 10; numSlices = 10; nDivs = numSlices;
pointAtToeVec = np.array([23, 3]); pointAtCrownVec = np.array([2, 15]);
slipRadius = 14; waterUnitWeight = 9.81; materialUnitWeight = 19.5;
frictionAngleGrad = 23; cohesion = 18; wantConstSliceWidthTrue = False;
# Previous functions
boundPointsCordsArray, fromToeOriginRowVec, coordTransMat = materialboundary\
    (slopeHeight, slopeDip, crownDist, toeDist)
surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec, \
    slopeHeight, slopeDip, crownDist, toeDist)
watertableDataCell, wtCoordsArray = defineswatertable(wtDepthAtCrown, \
    surfaceDataCell)
existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
    pointAtCrownVec, slipRadius)
slicesSTRCell = divideslipintoslices(slipArcSTR, surfaceDataCell, \
    watertableDataCell, numSlices, pointAtToeVec, pointAtCrownVec, \
    wantConstSliceWidthTrue)
# This function
print(interateffelleniussat(slicesSTRCell, waterUnitWeight, \
    materialUnitWeight, frictionAngleGrad, cohesion, slipRadius))

---
sf = interateffelleniussat(slicesSTRCell, waterUnitWeight, \
    materialUnitWeight, frictionAngleGrad, cohesion, slipRadius)
'''
def interateffelleniussat(slicesSTRCell, waterUnitWeight, \
    materialUnitWeight, frictionAngleGrad, cohesion, slipRadius):

    ## Transform information of slices structures into an array and display
    # input variables
    temp, reportedArray = reportslicestructurevalues(slicesSTRCell)

    numSlices = len(reportedArray[:,0])
    num = np.zeros(numSlices)
    
    # Obtain values from the array for further calculations
    #midPointArray = reportedArray[:,0:2]
    areaArray = reportedArray[:,2]
    widthArray =reportedArray[:,3];
    #midHeightArray =reportedArray[:,4]
    inclinationAngleGradAtBottomArray = reportedArray[:,5]
    inclinationAngleGradAtTopArray = reportedArray[:,6]
    wtMidHeightArray = reportedArray[:,7]
    wtMidHeightAboveSlopeArray = reportedArray[:,8]
    hrzMomentArm = reportedArray[:,9]
    vrtMomentArm = reportedArray[:,10]
     
    ## Precalculating some variables

    wtExternalPressureArray = wtMidHeightAboveSlopeArray*waterUnitWeight
    porePressureArray = wtMidHeightArray*waterUnitWeight

    ## Solve for the factor of safety
    fricAngTangent = np.tan(np.radians(frictionAngleGrad))
    alphaAngBottomSinArray = \
        np.sin(np.radians(inclinationAngleGradAtBottomArray))
    alphaAngBottomCosArray = \
        np.cos(np.radians(inclinationAngleGradAtBottomArray))
    BetaAngTopCosArray = \
        np.cos(np.radians(inclinationAngleGradAtTopArray))
    BetaAngTopSinArray = \
        np.sin(np.radians(inclinationAngleGradAtTopArray))
    angDifCosArray = np.cos(np.radians(inclinationAngleGradAtBottomArray-\
        inclinationAngleGradAtTopArray))
    
    lengthBaseArray = widthArray/alphaAngBottomCosArray
    
    # slice weights
    materialWeightArray = materialUnitWeight*areaArray
    externalWtForceArray = wtExternalPressureArray*widthArray/\
        BetaAngTopCosArray
    wtForceArray = porePressureArray*lengthBaseArray

    momentWtForce = externalWtForceArray*(BetaAngTopCosArray*hrzMomentArm+\
        BetaAngTopSinArray*vrtMomentArm)

    # final math          
    num = cohesion*lengthBaseArray+(materialWeightArray*\
        alphaAngBottomCosArray+externalWtForceArray*angDifCosArray-\
        wtForceArray*alphaAngBottomCosArray**2)*fricAngTangent
    
    den = materialWeightArray*alphaAngBottomSinArray
    
    sf = sum(num)/(sum(den)-sum(momentWtForce)/slipRadius)

    return sf
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
