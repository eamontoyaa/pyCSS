import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.optimize import brentq

from .defineslipcircle import defineslipcircle
from .defineswatertable import defineswatertable
from .divideslipintoslices import divideslipintoslices
from .interatefbishopsimpsat import interatefbishopsimpsat
from .interateffelleniussat import interateffelleniussat
from .materialboundary import materialboundary
from .obtainmaxdepthdist import obtainmaxdepthdist
from .plotslice import plotslice
from .reportslicestructurevalues import reportslicestructurevalues
from .sliparcdiscretization import sliparcdiscretization
from .terrainsurface import terrainsurface
from .vertprojection2pline import vertprojection2pline

'''
## Description:
Call other functions to find the minimum safety factor  for circular slip at 
each methods.

Plot a contours map to show distribution of safety factor values.

Obtain a text file with summary of analysis.

## External sub-function(s):

materialboundary, terrainsurface, vertprojection2pline, defineswatertable, 
defineslipcircle, sliparcdiscretization, obtainmaxdepthdist, 
vertprojection2pline, divideslipintoslices, interateffelleniussat,
interatefbishopsimpsat, plotslice, reportslicestructurevalues. 

# Input(s):
Name of project (projectName).

Name of project's author (projectAuthor).

Date of analysis (projectDate).

Height of the slope (slopeHeight).

Slope dip, given by a bidimensional vector which represents a vertical 
distance and a horizontal distance that not necesary representing the real 
slope distances [horzDist,vertDist], (slopeDip).

Crown horizontal plane distance (crownDist).

Toe horizontal plane distance (toeDist)

Logical variable for define if is wanted or not to generate automatic slope 
depth at toe (wantAutomaticToeDepth).

Slope depth at toe. (toeDepth).

Number of circular slip surfaces that to be evaluated (numCircles).

Length of each increment to be added to the initial radius (radiusIncrement)

Number of times that radius will be increased (numberIncrements)

Maximum number of safety factor that will be shown on contour graph
(maxFsValueCont)

Logical variable for define if is wanted or not a water table (wantWatertable)

Distance from the horizontal surface at the slope crown to the
watertable (wtDepthAtCrown).

Logical value put as 'True' or 'False' if it is wanted to consider the slope 
partially submerged, ie the foot slope is under the watertable 
(toeUnderWatertable).

Unit weight of the water (waterUnitWeight).

Geomaterial unit weight in dry state (materialUnitWeight).

Angle of friction of the geomaterial at the slice base (frictionAngleGrad).

Cohesion of the geomaterial at the slice base (cohesion).

Do you what to generate constant width slices, if so put it True
(wantConstSliceWidthTrue).

Number of slices one wants to disect the slip circle (numSlices).

Number of polylines that defines the arc (nDivs).

Label with method chosen for the analysis. Can be 'Flns' for Fellenius, 'Bshp' 
for Bishop or 'Allm' for both (methodString).

Label with output format of the output image of the analysis. Can be '.eps', 
'.jpeg', '.jpg', '.pdf', '.pgf', '.png', '.ps', '.raw', '.rgba', '.svg',
'.svgz', '.tif', or  '.tiff' (outputFormatImg).

## Output(s):
Image file with plot of problem/poject.

text file with summary of problem/poject.
'''
def automaticslipcircles(projectName, projectAuthor, projectDate, slopeHeight,\
        slopeDip, crownDist, toeDist, wantAutomaticToeDepth, toeDepth, \
        numCircles, radiusIncrement, numberIncrements, maxFsValueCont, \
        wantWatertable, wtDepthAtCrown, toeUnderWatertable, waterUnitWeight, \
        materialUnitWeight, frictionAngleGrad, cohesion, \
        wantConstSliceWidthTrue, numSlices, nDivs, methodString, \
        outputFormatImg):

    ## Previous considerations
    if wantAutomaticToeDepth == True:
        toeDepth = [obtainmaxdepthdist(slopeHeight[0], slopeDip, crownDist[0],\
    toeDist[0]), slopeHeight[1]]
    if wantWatertable == False:
        wtDepthAtCrown = [slopeHeight[0]+toeDepth[0], slopeHeight[1]]

    ## Define the problem boundary
    boundPointsCordsArray, tempFromToeOriginRowVec, coordTransMat = \
        materialboundary(slopeHeight[0], slopeDip, crownDist[0], toeDist[0])
    fromToeOriginRowVec = np.array([tempFromToeOriginRowVec[0], \
        toeDepth[0]])
    boundPointsCordsArray[2:-1,1] += -tempFromToeOriginRowVec[1]+\
        fromToeOriginRowVec[1]
    
    #--------------------------------------------------------------------------
    ## Define the surface polyline
    surfaceDataCell, surfaceChordsArray = terrainsurface(fromToeOriginRowVec,\
        slopeHeight[0], slopeDip, crownDist[0], toeDist[0])
    
    #--------------------------------------------------------------------------
    ## Define the water table polyline
    watertableDataCell, wtCoordsArray = defineswatertable(wtDepthAtCrown[0], \
        surfaceDataCell, toeUnderWatertable)
    
    #--------------------------------------------------------------------------    
    #Finding random points at crown an toe
    numberRandPairs = int(numCircles/numberIncrements)
    
    randNumbersForCrownTemp = np.random.rand(numberRandPairs)
    randNumbersForToeTemp = np.random.rand(numberRandPairs)
    
    hztSlopeLength = surfaceChordsArray[-1,0]-surfaceChordsArray[0,0]
    
    randNumbersForCrown = randNumbersForCrownTemp*hztSlopeLength/2
    randNumbersForToe = 0.5*hztSlopeLength*(randNumbersForToeTemp+1)
    
    #x and y-values for point when toe begining
    xValueAtToeBegin = surfaceChordsArray[2,0]
    yValueAtToeBegin = surfaceChordsArray[2,1]
    
    #Defining lists
    pointAtCrownVecList = []
    pointAtToeVecList = []
    slipArcSTRList = []
    arcPointsCoordsArrayList = []
    slicesSTRCellList = []
    reportCellList = []
    reportedArrayList = []
    fFelleniusSatList = []
    fBishopSimpleSatList = []
    centerList = []
    
    #Projecting random points on surface
    for i in range(numberRandPairs):
        pointAtCrownVec = vertprojection2pline(\
            np.array([randNumbersForCrown[i], 0]), surfaceDataCell)
        pointAtToeVec = vertprojection2pline(\
        np.array([randNumbersForToe[i], 0]), surfaceDataCell)
        
        ## Calculating initial and the other ones radius for iterations using 
        # same principle as obtainmaxdepthdist function        
        differenceVec = pointAtToeVec-pointAtCrownVec
        distExtrPts = np.sqrt(np.dot(differenceVec, differenceVec))
        initCircleRadius = distExtrPts/2*distExtrPts/differenceVec[0]+0.1

        radiusArray = np.zeros(numberIncrements)
        radiusArray[0] = initCircleRadius
        for i in range(1,numberIncrements):
            radiusArray[i] = radiusArray[i-1]+radiusIncrement[0]
        
        # iterating 
        for radius in radiusArray:
                   
            ## Define the slip circle strcuture
            existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
                pointAtCrownVec, radius)

            # verifying if is a valid slip circle
            if pointAtToeVec[0] > xValueAtToeBegin:
                yValueAtCirceOnToeBegin = -np.sqrt(radius**2-(\
                    xValueAtToeBegin-slipArcSTR['center'][0])**2)+\
                    slipArcSTR['center'][1]
                if yValueAtCirceOnToeBegin > yValueAtToeBegin:
                    # re-defining "pointAtToeVec" when the circle cuts the 
                    # slope face
                    def f(x):
                        return surfaceDataCell[1]['slope']*x+\
                        surfaceDataCell[1]['intercept']+np.sqrt(radius**2-\
                        (xValueAtToeBegin-slipArcSTR['center'][0])**2)-\
                        slipArcSTR['center'][1]
                    newRandNumberForToe = brentq(f, \
                        surfaceDataCell[1]['iniPtVec'][0], \
                        surfaceDataCell[1]['endPtVec'][0])
                    # new toe point
                    pointAtToeVec = vertprojection2pline(np.array([\
                        newRandNumberForToe, 0]), surfaceDataCell)

            # Adding slip circle data to lists
            pointAtCrownVecList += [pointAtCrownVec]
            pointAtToeVecList += [pointAtToeVec]
            slipArcSTRList += [slipArcSTR]
            centerList += [slipArcSTR['center']]
            
            ## Define the slip circle coordinates
            arcPointsCoordsArray = sliparcdiscretization(pointAtToeVec, \
                pointAtCrownVec, nDivs, slipArcSTR)
            arcPointsCoordsArrayList += [arcPointsCoordsArray]
            
            #--------------------------------------------------------------  
            ## Create the slices cell
            slicesSTRCell = divideslipintoslices(slipArcSTR, \
                surfaceDataCell, watertableDataCell, numSlices, \
                pointAtToeVec, pointAtCrownVec, wantConstSliceWidthTrue)
            slicesSTRCellList += [slicesSTRCell]
    
            #--------------------------------------------------------------  
            ## Summarizing the data of slice structures 
            reportCell, reportedArray = reportslicestructurevalues(\
                slicesSTRCell)
            reportCellList += [reportCell]
            reportedArrayList += [reportedArray]
            
            #--------------------------------------------------------------  
            ## Interate the safety factor for all methods
                
            # Method 1: Function that calculates by the Fellenius Method.
            fFelleniusSat = interateffelleniussat(slicesSTRCell, \
                waterUnitWeight[0], materialUnitWeight[0], \
                frictionAngleGrad[0], cohesion[0], radius)
            fFelleniusSatList += [fFelleniusSat]
            # Method 2: Function that calculates fs by the simplyfied 
            # Bishop method.
            fBishopSimpleSat = interatefbishopsimpsat(slicesSTRCell, \
                waterUnitWeight[0], materialUnitWeight[0], \
                frictionAngleGrad[0], cohesion[0], radius, \
                fFelleniusSat)
            fBishopSimpleSatList += [fBishopSimpleSat]
    
    #--------------------------------------------------------------------------        
    # Minimum FS with Fellenius method
    indesxSwediwsMethod = fFelleniusSatList.index(min(fFelleniusSatList))
    pointAtCrownVecFellenius = pointAtCrownVecList[indesxSwediwsMethod]
    pointAtToeVecFellenius = pointAtToeVecList[indesxSwediwsMethod]
    slipArcSTRFellenius = slipArcSTRList[indesxSwediwsMethod]
    arcPointsCoordsArrayFellenius = arcPointsCoordsArrayList[indesxSwediwsMethod]
    slicesSTRCellFellenius = slicesSTRCellList[indesxSwediwsMethod]
    reportCellFellenius = reportCellList[indesxSwediwsMethod]
    fFelleniusSat = fFelleniusSatList[indesxSwediwsMethod]
    centerFellenius = centerList[indesxSwediwsMethod]
    
    #---------------------------------------------------alguien que apenas le habla-----------------------
    # Minimum FS with Bishop's method
    indesxBishopMethod = fBishopSimpleSatList.index(min(fBishopSimpleSatList))
    pointAtCrownVecBishop = pointAtCrownVecList[indesxBishopMethod]
    pointAtToeVecBishop = pointAtToeVecList[indesxBishopMethod]    
    slipArcSTRBishop = slipArcSTRList[indesxBishopMethod]
    arcPointsCoordsArrayBishop =arcPointsCoordsArrayList[indesxBishopMethod]
    slicesSTRCellBishop = slicesSTRCellList[indesxBishopMethod]
    reportCellBishop = reportCellList[indesxBishopMethod]
    fBishopSimpleSat = fBishopSimpleSatList[indesxBishopMethod]
    centerBishop = centerList[indesxBishopMethod]
    
    #--------------------------------------------------------------------------
    ## Values for contour graph
    correctIndexesFellenius = []
    for i in fFelleniusSatList:
        if np.isnan(i) == True or i>maxFsValueCont:
            correctIndexesFellenius += [False]
        else:
            correctIndexesFellenius += [True]
    correctCenterFellenius = np.vstack(np.array(centerList)[np.array(\
        correctIndexesFellenius)])
    correctFelleniusValues = np.array(fFelleniusSatList)[np.array(\
        correctIndexesFellenius)]

    correctIndexesBishop = []
    for i in fFelleniusSatList:
        if np.isnan(i) == True or i>maxFsValueCont:
            correctIndexesBishop += [False]
        else:
            correctIndexesBishop += [True]
    correctCenterBishop = np.vstack(np.array(centerList)[np.array(\
        correctIndexesBishop)])
    correctBishopValues = np.array(fFelleniusSatList)[np.array(\
        correctIndexesBishop)]
    #--------------------------------------------------------------------------
    ## Answering some questions
    if toeUnderWatertable == True:
        slopeSubmergedAns = 'Yes'
    else:
        slopeSubmergedAns = 'No'
    if wantConstSliceWidthTrue == True:
        constantSliceWidthAns = 'Yes'
    else:
        constantSliceWidthAns = 'No'
    
    #--------------------------------------------------------------------------
    ## Plotting the problem
    ### First figure (Fellenius method)
    plt.figure(str(np.random.rand()))
    # plt.hold(True)
    plt.subplot(1,2,1)
    # plt.hold(True)
    plt.grid(True)
    plt.title('Fellenius Method')
    # Plot the circular arc center.
    plt.plot(centerFellenius[0], centerFellenius[1], 'k.', lw=7)
    # Plot the slip circular arc.
    plt.plot(arcPointsCoordsArrayFellenius[:,0], \
        arcPointsCoordsArrayFellenius[:,1], 'k-', lw=0.3)
    # Plot the slices.
    for i in range(len(slicesSTRCellFellenius)):
        plotslice(slicesSTRCellFellenius[i])
    # Plot the material boundary and the slope geometry.
    plt.plot(boundPointsCordsArray[:,0], boundPointsCordsArray[:,1], 'k-')
    # Plot the water table.
    plt.plot(wtCoordsArray[:,0], wtCoordsArray[:,1], 'b-')
    # Plot the terrain surface.
    plt.plot(surfaceChordsArray[:,0], surfaceChordsArray[:,1], 'k', lw=2)
    # Plot the factor of safety value in graphic.
    fsText = ' $f_{\mathrm{s}\, \mathrm{Min.}}=$'+\
        format(fFelleniusSat, '.3f')
    plt.text(0, max(correctCenterFellenius[:,1]), fsText, fontsize = 10, \
        horizontalalignment='left', verticalalignment='top')
    # Plot the radius of the arc at both ends.
    radius1PlotArrayFellenius = np.vstack((centerFellenius, \
        pointAtToeVecFellenius))
    plt.plot(radius1PlotArrayFellenius[:,0], radius1PlotArrayFellenius[:,1], \
        'k-', lw=1)
    radius2PlotArrayFellenius = np.vstack((centerFellenius, \
        pointAtCrownVecFellenius))
    plt.plot(radius2PlotArrayFellenius[:,0], radius2PlotArrayFellenius[:,1], \
        'k-', lw=1)    
    # Plot SF contourns
    x = correctCenterFellenius[:,0]
    y = correctCenterFellenius[:,1]
    triang = tri.Triangulation(x, y)
    plt.tricontour(triang, correctFelleniusValues, 10, linewidths=0.15, \
        colors='k')
    plt.tricontourf(triang, correctFelleniusValues, 10, cmap=plt.cm.jet_r)
    plt.colorbar(aspect=15, orientation='horizontal', format='%.1f')
    
    ## Final plot details.
    plt.axis('equal')
    plt.xlabel('$x$ distance')
    plt.ylabel('$y$ distance')
    
    ### Second figure (Bishop method)
    plt.subplot(1,2,2)
    # plt.hold(True)
    plt.grid(True)
    plt.title('Bishop Simp. Method')
    # Plot the circular arc center.
    plt.plot(centerBishop[0], centerBishop[1], 'k.', lw=7)
    # Plot the slip circular arc.
    plt.plot(arcPointsCoordsArrayBishop[:,0], \
        arcPointsCoordsArrayBishop[:,1], 'k-', lw=0.3)
    # Plot the slices.
    for i in range(len(slicesSTRCellBishop)):
        plotslice(slicesSTRCellBishop[i])
    # Plot the material boundary and the slope geometry.
    plt.plot(boundPointsCordsArray[:,0], boundPointsCordsArray[:,1], 'k-')
    # Plot the water table.
    plt.plot(wtCoordsArray[:,0], wtCoordsArray[:,1], 'b-')
    # Plot the terrain surface.
    plt.plot(surfaceChordsArray[:,0], surfaceChordsArray[:,1], 'k', lw=2)
    # Plot the factor of safety value in graphic.
    fsText = ' $f_{\mathrm{s}\, \mathrm{Min.}}=$'+\
        format(fBishopSimpleSat, '.3f')
    plt.text(0, max(correctCenterBishop[:,1]), fsText, fontsize = 10, \
        horizontalalignment='left', verticalalignment='top')
    # Plot the radius of the arc at both ends.
    radius1PlotArrayBishop = np.vstack((centerBishop, \
        pointAtToeVecBishop))
    plt.plot(radius1PlotArrayBishop[:,0], radius1PlotArrayBishop[:,1], 'k-', \
        lw=1)
    radius2PlotArrayBishop = np.vstack((centerBishop, \
        pointAtCrownVecBishop))
    plt.plot(radius2PlotArrayBishop[:,0], radius2PlotArrayBishop[:,1], 'k-', \
        lw=1)    
    # Plot SF contourns
    x = correctCenterBishop[:,0]
    y = correctCenterBishop[:,1]
    triang = tri.Triangulation(x, y)
    plt.tricontour(triang, correctBishopValues, 10, linewidths=0.15, colors='k')
    plt.tricontourf(triang, correctBishopValues, 10, cmap=plt.cm.jet_r)
    plt.colorbar(aspect=15, orientation='horizontal', format='%.1f')
    
    ## Final plot details.
    plt.axis('equal')
    plt.xlabel('$x$ distance')
    #plt.ylabel('$y$ distance')
    plt.savefig(projectName+outputFormatImg, dpi=300)
    # plt.hold(False)
    #------------------------------------------------------------------------------
    ## Exporting summary data
    outFile = open(projectName+'.txt', 'w')
    outFile.write(\
        '---SUMMARY OF PROJECT---\n \n'+\
        'Project name: '+projectName+'\n'+\
        'Author: '+projectAuthor+'\n'+\
        'Date: '+str(projectDate)+'\n'+\
        'Minimum safety factors: \n'+\
        '    -Fellenius method: '+str(fFelleniusSat)+'\n'+\
        '    -Bishop method: '+str(fBishopSimpleSat)+'\n'+\
        'Number of surfaces evaluated: '+str(numCircles)+'\n \n'+\
        '--Slope geometry--\n'+\
        'Height: '+str(slopeHeight[0])+' '+slopeHeight[1]+'\n'+\
        'Dip: '+str(np.degrees(np.tan(slopeDip[1]/slopeDip[0])))+' degrees\n'+\
        'Crown distance: '+str(crownDist[0])+' '+crownDist[1]+'\n'+\
        'Toe distance: '+str(toeDist[0])+' '+toeDist[1]+'\n'+\
        'Toe depth: '+str(toeDepth[0])+' '+toeDepth[1]+'\n'+\
        'Surface coordinates: \n'+str(surfaceChordsArray)+'\n \n'+\
        '--Watertable geometry--\n'+\
        'Depth at crown: '+str(wtDepthAtCrown[0])+' '+wtDepthAtCrown[1]+'\n'+\
        'Is the slope partially submerged? '+slopeSubmergedAns+'\n'+\
        'Watertable coordinates: \n'+str(wtCoordsArray)+'\n \n'+\
        '--Materials properties--\n'+\
        'Water unit weight: '+str(waterUnitWeight[0])+' '+waterUnitWeight[1]+\
            '\n'+\
        'Soil unit weight: '+str(materialUnitWeight[0])+' '+\
            materialUnitWeight[1]+'\n'+\
        'Friction angle '+str(frictionAngleGrad[0])+' '+frictionAngleGrad[1]+\
            '\n'+\
        'Cohesion: '+str(cohesion[0])+' '+cohesion[1]+'\n \n'+\
        '--Slip circle description for minimun safety factor found with \n'+
            'Fellenius Method-- \n'+\
        'Radius: '+str(slipArcSTRFellenius['radius'])+' '+slopeHeight[1]+'\n'+\
        'Center coordinates: '+str(slipArcSTRFellenius['center'])+'\n \n'+\
        '--Slices data--\n'+\
        'Number of slices: '+str(numSlices)+'\n'+\
        'Has the surface slip constant width slices? '+\
            constantSliceWidthAns+'\n \n'+\
        'Slices structures data: \n'+\
        str(reportCellFellenius)+'\n \n'+\
        '--Slip circle description for minimun safety factor found with \n'+
            'Bishop Method-- \n'+\
        'Radius: '+str(slipArcSTRBishop['radius'])+' '+slopeHeight[1]+'\n'+\
        'Center coordinates: '+str(slipArcSTRBishop['center'])+'\n \n'+\
        '--Slices data--\n'+\
        'Number of slices: '+str(numSlices)+'\n'+\
        'Has the surface slip constant width slices? '+\
            constantSliceWidthAns+'\n \n'+\
        'Slices structures data: \n'+\
        str(reportCellBishop)+'\n \n'+\
        'Note: This program calculated the safety factor to circular slip,\n'+\
        'under limit equilibrium considerations, using Fellenius and Bishop'+\
        '\nmethods. The imagen attached shows the calculation performed.\n\n'+\
        'This program is distributed in the hope that it will be useful, \n'+\
        'but WITHOUT ANY WARRANTY; without even the implied warranty of \n'+\
        'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.')
    outFile.close()
    return


get_min_fos = automaticslipcircles

''''
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
