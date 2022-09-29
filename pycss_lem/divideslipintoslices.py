# import modules
import numpy as np
from .sliparcdiscretization import sliparcdiscretization
from .uniquewithtolerance import uniquewithtolerance
from .vertprojection2pline import vertprojection2pline
from .tangentlineatcirclept import tangentlineatcirclept
from .extractplinefrom2pts import extractplinefrom2pts
from .polyarea import polyarea

'''
# Description:
Divides the slip circular arc into the respective required number of
slices according to the surface--terrain configuration, and creates the
slices data structure with all the useful data in order to perform any
further limit equilibrium slip analysis.

# External sub-function(s):
sliparcdiscretization, uniquewithtolerance, vertprojection2pline,
tangentlineatcirclept, extractplinefrom2pts, polyarea. 

# Input(s):
Dictionary type slip circle structure (slipArcSTR) which contains the 
following fields:
      center: center of the slip arc;
      radius: radius of the slip arc;
  iniAngGrad: initial angle in hexagesimal degrees of the slop arc;
  endAngGrad: final angle in hexagesimal degrees of the slop arc;
    deepDist: deepest vertical distance in respecto to the surface;
    leftDist: backwards distance formo the center vertical.
Values of the coordiantes are relative to the global coordinate system.

List containinig lines structures of the surface terrain
(surfaceDataCell), each line structure has the following fields:
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
Values of the coordiantes are relative to the global coordinate system.

Similar to 'surfaceDataCell', this variable contains data of a plyline
but that represents the water table surface (watertableDataCell). In each
element of the list is a dictionary type line structure with the same 
variables as the strucures of 'surfaceDataCell' (watertableDataCell).

Number of slices one wants to disect the slip circle (numSlices).

Two dimensional vector of the coordinates that defines the slip at the
slope toe (pointAtToeVec);

Two dimensional vector of the coordinates that defines the slip at the
slope crown (pointAtCrownVec);

Do you what to generate constant width slices, if so put it True
(wantConstSliceWidthTrue). Default value is False.

# Output(s):
List containing all the slices dictionary type structures (slicesSTRCell). 
Each slice structure has the following fields:
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

## Example1:
# inputs:
slopeHeight = 12.0; slopeDip = np.array([1, 2.5]); crownDist = 10.0
toeDist = 10.0; wtDepthAtCrown = 0; numSlices = 10; slipRadius = 15
pointAtToeVec = np.array([23, 3.3]); pointAtCrownVec = np.array([2, 15.3])
# Previous functions
boundPointsCordsArray, fromToeOriginRowVec, coordTransMat = \
    materialboundary(slopeHeight, slopeDip, crownDist, toeDist)
surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec,\
    slopeHeight, slopeDip, crownDist, toeDist)
watertableDataCell, wtCoordsArray = defineswatertable(wtDepthAtCrown, 
    surfaceDataCell)
existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
    pointAtCrownVec, slipRadius)
# This function
slicesSTRCell = divideslipintoslices(slipArcSTR, \
    surfaceDataCell, watertableDataCell, numSlices, pointAtToeVec, \
    pointAtCrownVec)
---
slicesSTRCell = divideslipintoslices(slipArcSTR, surfaceDataCell, \
    watertableDataCell, numSlices, pointAtToeVec, pointAtCrownVec, \
    wantConstSliceWidthTrue = False)
'''
def divideslipintoslices(slipArcSTR, surfaceDataCell, watertableDataCell, \
    numSlices, pointAtToeVec, pointAtCrownVec, \
    wantConstSliceWidthTrue = False):

    ## Obtaining the coordiantes of the slip surface    
    slipChordsArray = sliparcdiscretization(pointAtToeVec, pointAtCrownVec, \
        numSlices, slipArcSTR)
    
    ## Diserning between doing a calculation of equal or non--equal width slices
    if wantConstSliceWidthTrue == False:
        #Do calculation in order to divide the slip surface into non--equal
        #slices but coinciding with surfaces bifurcations points
    
        #Coordiantes array of terrain surface
        numLines = len(surfaceDataCell)
        terrainChordsArray = np.zeros((numLines+1,2))
        for i in range(numLines):
            tlineSTR = surfaceDataCell[i]
            terrainChordsArray[i,:] = tlineSTR['iniPtVec']
        terrainChordsArray[-1,:] = tlineSTR['endPtVec']
        #Terrain coordiantes between the limits of the slip surface
        #lower boundary
        indexesIniVec = terrainChordsArray[:,0] >= slipChordsArray[-1,0]
        terrainChordsInsideSlipArray = terrainChordsArray[indexesIniVec,:]
        #upper boundary
        indexesEndVec = terrainChordsInsideSlipArray[:,0] <= \
            slipChordsArray[0,0]
        terrainChordsInsideSlipArray = terrainChordsInsideSlipArray\
            [indexesEndVec,:]
        #Obtaining the y--coordiante at the slip of the terrain points
        xCoordsArray = terrainChordsInsideSlipArray[:,0]
        yCoordsArray = slipArcSTR['center'][1]-np.sqrt(slipArcSTR['radius']**2\
            -(xCoordsArray-slipArcSTR['center'][0])**2)
        addedTerrainSlipChoordsArray = np.transpose(np.array([xCoordsArray, \
            yCoordsArray]))
        
        #Coordiantes array of water table surface
        wtNumLines = len(watertableDataCell)
        watertableChordsArray = np.zeros((wtNumLines+1,2))
        for i in range(wtNumLines):
            wlineSTR = watertableDataCell[i]
            watertableChordsArray[i,:] = wlineSTR['iniPtVec']
        watertableChordsArray[-1,:] = wlineSTR['endPtVec']
        #Water table coordiantes between the limits of the slip surface
        #lower boundary
        indexesIniVec = watertableChordsArray[:,0] >= slipChordsArray[-1,0]
        watertableChordsInsideSlipArray = watertableChordsArray[indexesIniVec,\
            :]
        #upper boundary
        indexesEndVec = watertableChordsInsideSlipArray[:,0] <= \
            slipChordsArray[0,0]
        watertableChordsInsideSlipArray = watertableChordsInsideSlipArray\
            [indexesEndVec,:]
        #Obtaining the y--coordiante at the slip of the terrain points
        xCoordsArray = watertableChordsInsideSlipArray[:,0]
        yCoordsArray = slipArcSTR['center'][1]-np.sqrt(slipArcSTR['radius']**2\
            -(xCoordsArray-slipArcSTR['center'][0])**2)
        addedWatertableSlipChoordsArray = np.transpose(np.array([xCoordsArray,\
            yCoordsArray]))
    
        #Joining the bifurcation points
        totalInsideSlipArray = np.concatenate((slipChordsArray, \
            addedTerrainSlipChoordsArray, addedWatertableSlipChoordsArray), 0)
        #totalInsideSlipArray =unique( totalInsideSlipArray ,'rows' );
        totalInsideSlipArray = uniquewithtolerance(totalInsideSlipArray, 0.01)
        
    else:
        #Do calculation in order to divide the slip surface into equal width
        #slices
        totalInsideSlipArray = uniquewithtolerance(slipChordsArray, 0.01)

#------------------------------------------------------------------------------    
    ## Obtain coordiantes from slip surface to the surface terrain
    numberOfSlipPoints = len(totalInsideSlipArray[:,0])
    totalTerrainFromSlipArray = np.zeros((numberOfSlipPoints,2))
    for i in range(numberOfSlipPoints):
        totalTerrainFromSlipArray[i,:] = vertprojection2pline\
            (totalInsideSlipArray[i,:], surfaceDataCell)
    
    # Obtaining the arrays for calculations
    newNumSlices = len(totalInsideSlipArray[:,0])-1
    
    # Obtaining coordiantes of initial and end points coordinates at slip
    # surface
    slicesIniPointsArray = totalInsideSlipArray[0:-1,:]
    slicesEndPointsArray = totalInsideSlipArray[1:,:]
    
    # Obtaining coordiantes of initial and end points coordiantes at terrain
    # surface
    terrainIniPointsArray = totalTerrainFromSlipArray[0:-1,:]
    terrainEndPointsArray = totalTerrainFromSlipArray[1:,:]
    
    # Extreme vertical borders slice heights
    slicesIniHeightArray = terrainIniPointsArray[:,1]-slicesIniPointsArray[:,1]
    slicesEndHeightArray = terrainEndPointsArray[:,1]-slicesEndPointsArray[:,1]
    
    ## Coordiantes of slices mid points.
    slicesMidPointsArray = np.zeros((newNumSlices, 2))
    slicesMidPointsArray[:,0] = 0.5*(slicesEndPointsArray[:,0]+\
        slicesIniPointsArray[:,0])
    slicesMidPointsArray[:,1] = 0.5*(slicesEndPointsArray[:,1]+\
        +slicesIniPointsArray[:,1])
    
    ## Slice material heights are each the mean of initial, final and middle.
    # Terrain heights.
    sliceProjOrdinateArray = np.zeros(newNumSlices);
    for i in range(newNumSlices):
        tempo00 = vertprojection2pline(slicesMidPointsArray[i,:], \
            surfaceDataCell)
        sliceProjOrdinateArray[i] = tempo00[1]
    sliceProjHeightArray = sliceProjOrdinateArray-slicesMidPointsArray[:,1]
    # The used slice height at middle point.
    sliceHeightArray = 1/3*(sliceProjHeightArray+slicesIniHeightArray+\
        slicesEndHeightArray)
    ## Slice material width.
    sliceWidthArray = slicesEndPointsArray[:,0]-slicesIniPointsArray[:,0]
    
#------------------------------------------------------------------------------    
    ## Obtain coordiantes from slip surface to the water table surface.
    totalWatertableFromSlipArray = np.zeros((numberOfSlipPoints, 2))
    for i in range(numberOfSlipPoints):
        totalWatertableFromSlipArray[i,:] = vertprojection2pline\
            (totalInsideSlipArray[i,:], watertableDataCell)

    # Obtaining coordiantes of initial and end point at water--table surface.
    watertableIniPointsArray = totalWatertableFromSlipArray[0:-1,:]
    watertableEndPointsArray = totalWatertableFromSlipArray[1:,:]
    
    # Extreme vertical borders slice heights.
    slicesWtIniHeightArray = watertableIniPointsArray[:,1]-\
        slicesIniPointsArray[:,1]
    slicesWtEndHeightArray = watertableEndPointsArray[:,1]-\
        slicesEndPointsArray[:,1]
    
    # Slice water heights are each the mean of initial, final and middle
    # water table heights.
    
    sliceWtProjOrdinateArray = np.zeros(newNumSlices)
    for i in range(newNumSlices):
        tempo01 = vertprojection2pline(slicesMidPointsArray[i,:], \
            watertableDataCell)
        sliceWtProjOrdinateArray[i] = tempo01[1]
    sliceWtProjHeightArray = sliceWtProjOrdinateArray-slicesMidPointsArray[:,1]
    
    # The used slice water table height at middle point.
    sliceWtHeightArray = 1/3*(sliceWtProjHeightArray+slicesWtIniHeightArray+\
        slicesWtEndHeightArray)
    # Negative values are transformed to cero.
    indexesLessCero = sliceWtHeightArray < 0
    sliceWtHeightArray[indexesLessCero] = 0

#------------------------------------------------------------------------------
    ## Water column height above the surface of the slope
    wtHeightAboveSlope = sliceWtHeightArray-sliceHeightArray
    # Negative values are transformed to cero.
    indexesLessCero = wtHeightAboveSlope < 0
    wtHeightAboveSlope[indexesLessCero] = 0
    
    hrzMomentArm = slicesMidPointsArray[:,0]-slipArcSTR['center'][0]
    vrtMomentArm = -1*(slicesMidPointsArray[:,1]+sliceHeightArray-\
        slipArcSTR['center'][1])

#------------------------------------------------------------------------------    
    ## Slice inclinations angle at their bottoms.
    # They will be the slice--surface secant inclination in hexagesima degrees.
    
    # If the slice is drawn from left to right (which is the case), then
    # slideOrientationSign =-1
    slideOrientationSign =-1;
    
    sliceSurfaceSecIncliGradArray = np.degrees(slideOrientationSign*np.arctan(\
        (totalInsideSlipArray[1:,1]-totalInsideSlipArray[:-1,1])/(\
        totalInsideSlipArray[1:,0]-totalInsideSlipArray[:-1,0])))
    
    ## The slice--surface tangent inclination in hexagesimal degrees.
    sliceSurfaceTanIncliGradArray = np.zeros(newNumSlices)
    # The used slice--surface inclination in hexagesimal degrees.
    for i in range(newNumSlices):
       temp, tangentLineSTR = tangentlineatcirclept(slicesMidPointsArray[i,:],\
           slipArcSTR)
       sliceSurfaceTanIncliGradArray[i] = np.degrees(np.arctan(tangentLineSTR\
           ['slope']))

    # The slice--surface inclinations is those tangent to the circle at slice
    # middle point.
    errorTanGradArray = 0.5*abs(-1*sliceSurfaceTanIncliGradArray-\
        sliceSurfaceSecIncliGradArray)
    
    sliceSurfaceIncliGradArray = sliceSurfaceSecIncliGradArray[:]
    
#------------------------------------------------------------------------------     
    ## Slice inclinations angle at their top.
   
    sliceTopIncliGradArray = np.degrees(slideOrientationSign*np.arctan(\
        (totalTerrainFromSlipArray[1:,1]-totalTerrainFromSlipArray[:-1,1])/(\
        totalTerrainFromSlipArray[1:,0]-totalTerrainFromSlipArray[:-1,0])))
        
#------------------------------------------------------------------------------     
    ## Slices structures stored in a cell
    slicesSTRCell = []
    
    for i in range(newNumSlices):
        # Extract polyline beetween two extreme points.
        tempo01 = slicesIniPointsArray[i,1]+slicesIniHeightArray[i]
        tempo02 = slicesEndPointsArray[i,1]+slicesEndHeightArray[i]
        baseSlicePlineCordsArray = np.concatenate((
            [np.array([slicesIniPointsArray[i,0], tempo01])],
            [slicesIniPointsArray[i,:]],
            [slicesMidPointsArray[i,:]],
            [slicesEndPointsArray[i,:]],
            [np.array([slicesEndPointsArray[i,0], tempo02])]), 0)
        
        terrainSlicePlineCordsArray = extractplinefrom2pts\
            (slicesIniPointsArray[i,:], slicesEndPointsArray[i,:],\
            surfaceDataCell)
        
        if len(terrainSlicePlineCordsArray[1:-1,:]) == 0:
            completeSlicePlineCordsArray = np.concatenate((
                baseSlicePlineCordsArray,
                baseSlicePlineCordsArray[0:1,:]), 0)
        else:
            completeSlicePlineCordsArray = np.concatenate((
                baseSlicePlineCordsArray,
                terrainSlicePlineCordsArray[1:-1,:],
                baseSlicePlineCordsArray[0:1,:]), 0)            
        
        sliceSTR = {
            'plineCords': completeSlicePlineCordsArray[:],
            'area': polyarea(completeSlicePlineCordsArray[0:-1,0],\
                completeSlicePlineCordsArray[0:-1,1]),
            'midPoint': slicesMidPointsArray[i,:],
            'midHeight': sliceHeightArray[i],
            'width': sliceWidthArray[i],
            'inclinationAngleGradAtBottom': sliceSurfaceIncliGradArray[i],
            'inclinationAngleGradAtTop': sliceTopIncliGradArray[i],
            'wtMidHeight': sliceWtHeightArray[i],
            'wtMidHeightAboveSlope': wtHeightAboveSlope[i],
            'hrzMomentArm': hrzMomentArm[i],
            'vrtMomentArm': vrtMomentArm[i]}
        
        slicesSTRCell += [sliceSTR]

    return slicesSTRCell
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
