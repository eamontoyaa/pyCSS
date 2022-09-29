## import modules and functions
import os

import numpy as np
import matplotlib

if not os.environ.get('DISPLAY'):
    print('No display found. Using non-interactive Agg backend')
    matplotlib.use('Agg')

import matplotlib.pyplot as plt

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
Calls the other functions to evaluate the slope stability in only one 
circular slip surface.

Plots the scheme that represents the problem analysed.

Obtain a text file with summary of analysis.

## External sub-function(s):

materialboundary, terrainsurface, obtainmaxdepthdist, defineswatertable, 
defineslipcircle, sliparcdiscretization, vertprojection2pline, 
divideslipintoslices, interateffelleniussat,
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

Horizontal length of the first point of the circle (which is closer to the 
crown), measured from the end of the crown, right where the inclined surface
of the slope begins. Points to the left are negative and to the right are 
positive. (hztDistPointAtCrownFromCrown).

Horizontal length of the second point of the circle (which is closer to the 
toe), measured from the end of the crown, right where the inclined surface
of the slope begins. Only are allowed points to the right, therefore they are 
positive. (hztDistPointAtToeFromCrown).

Length of the slip circle radius (slipRadius).

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
Message which shows if analysis was reached or not (msg).

Image file with plot of problem/poject.

text file with summary of problem/poject.
---
msg = onlyonecircle(projectName, projectAuthor, projectDate, slopeHeight, \
    slopeDip, crownDist, toeDist, wantAutomaticToeDepth, toeDepth, \
    hztDistPointAtCrownFromCrown, hztDistPointAtToeFromCrown, \
    slipRadius, wantWatertable, wtDepthAtCrown, toeUnderWatertable, \
    waterUnitWeight, materialUnitWeight, frictionAngleGrad, cohesion, \
    wantConstSliceWidthTrue, numSlices, nDivs, methodString, \
    outputFormatImg)
'''
def onlyonecircle(projectName, projectAuthor, projectDate, slopeHeight, \
        slopeDip, crownDist, toeDist, wantAutomaticToeDepth, toeDepth, \
        hztDistPointAtCrownFromCrown, hztDistPointAtToeFromCrown, \
        slipRadius, wantWatertable, wtDepthAtCrown, toeUnderWatertable, \
        waterUnitWeight, materialUnitWeight, frictionAngleGrad, cohesion, \
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
    ## Verifying if surface inputs are corrects
    option = 0
    correctSurfaceSlopeInputs = True
    # Verifying if poits at surface are on surface
    hztSlopeLength = surfaceChordsArray[-1,0]-surfaceChordsArray[0,0]
    if hztDistPointAtCrownFromCrown[0] < -1*crownDist[0] or \
        hztDistPointAtToeFromCrown[0] > hztSlopeLength-crownDist[0]:
        correctSurfaceSlopeInputs = False
        option = 1
    # Verifying minimum radius
    if option == 0:
        ## Define the circle points at crown and toe
        pointAtCrownVec = vertprojection2pline(\
            np.array([hztDistPointAtCrownFromCrown[0]+\
            surfaceChordsArray[1][0], 0]), surfaceDataCell)
        pointAtToeVec = vertprojection2pline(\
            np.array([hztDistPointAtToeFromCrown[0]+surfaceChordsArray[1][0], \
            0]), surfaceDataCell)
        differenceVec = pointAtToeVec-pointAtCrownVec
        distExtrPts = np.sqrt(np.dot(differenceVec, differenceVec))
        minCircleRadius = distExtrPts/2*distExtrPts/differenceVec[0]+0.05
        if slipRadius[0] < minCircleRadius:
            correctSurfaceSlopeInputs = False
            option = 2
        # Verifying length of radius
        if distExtrPts/2 > slipRadius[0]:
            correctSurfaceSlopeInputs = False
            option = 3
        # Verifying intersection with slope face
        else:
            #------------------------------------------------------------------
            ## Define the slip circle polyline
            existSlipCircleTrue, slipArcSTR = defineslipcircle(pointAtToeVec, \
                pointAtCrownVec, slipRadius[0])    
            #x and y-values for point when toe begining
            xValueAtToeBegin = surfaceChordsArray[2,0]
            yValueAtToeBegin = surfaceChordsArray[2,1]    
            # verifying if is a valid slip circle
            if pointAtToeVec[0] > xValueAtToeBegin:
                yValueAtCirceOnToeBegin = -np.sqrt(slipRadius[0]**2-(\
                    xValueAtToeBegin-slipArcSTR['center'][0])**2)+\
                    slipArcSTR['center'][1]
                if yValueAtCirceOnToeBegin > yValueAtToeBegin:
                    correctSurfaceSlopeInputs = False
                    option = 4
    
    #--------------------------------------------------------------------------
    ## Choosing ways if slope surface's inputs are correct
    if correctSurfaceSlopeInputs == False and option == 1:
        msg = 'Slope surface\'s inputs are incorrect. One or both points '+\
            'which define circle surface is/are out surface; check it!'
        print(msg)
    elif correctSurfaceSlopeInputs == False and option == 2:
        msg = 'Slope surface\'s inputs are incorrect. The radius is shorter '+\
            'than minimum \nadmissible; check it!'
        print(msg)
    elif correctSurfaceSlopeInputs == False and option == 3:
        msg = 'Slope surface\'s inputs are incorrect. Radius input is '+\
            'shorter than minimum to define a circle; check it!'
        print(msg)
    elif correctSurfaceSlopeInputs == False and option == 4:
        msg = 'Slope surface\'s inputs are incorrect. The points at surface '+\
            'and radius \ndefine a circle that intercept the slope surface '+\
            'and toe simultaneously; check it!'
        print(msg)
    else:
        msg = 'Analysis successfully!'
        print(msg)
        ## Continue defining the slip circle polyline
        arcPointsCoordsArray = sliparcdiscretization(pointAtToeVec, \
        pointAtCrownVec, nDivs, slipArcSTR)
        
        #----------------------------------------------------------------------
        ## Create the slices cell
        slicesSTRCell = divideslipintoslices(slipArcSTR, \
            surfaceDataCell, watertableDataCell, numSlices, pointAtToeVec, \
            pointAtCrownVec, wantConstSliceWidthTrue)
        
        #----------------------------------------------------------------------
        ## Summarizing the data of slice structures 
        reportCell, reportedArray = reportslicestructurevalues(slicesSTRCell)
            
        #----------------------------------------------------------------------
        ## Interate the safety factor for all methods
        numberMethods = 2
        fsSatCell = np.zeros(numberMethods)
            
        # Method 1: Function that calculates by the Fellenius Method.
        fFelleniusSat = interateffelleniussat(slicesSTRCell, \
            waterUnitWeight[0], materialUnitWeight[0], frictionAngleGrad[0], \
            cohesion[0], slipRadius[0])
        fsSatCell[0] = fFelleniusSat
        
        # Method 2: Function that calculates fs by the simplyfied Bishop method
        fBishopSimpleSat = interatefbishopsimpsat(slicesSTRCell, \
            waterUnitWeight[0], materialUnitWeight[0], frictionAngleGrad[0], \
            cohesion[0], slipRadius[0], fFelleniusSat)
        fsSatCell[1] = fBishopSimpleSat
        
        # Select the method to calcualte the safety factor.
        if methodString == 'Flns':
            selectedFs = fsSatCell[0]
        elif methodString == 'Bshp':
            selectedFs = fsSatCell[1]
        else: 
            selectedFs = fsSatCell
            methodString = 'Allm'
        
        #----------------------------------------------------------------------
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
        plt.figure(str(np.random.rand()))
        # plt.hold(True)
        plt.grid(True)
        # Plot the circular arc center.
        plt.plot(slipArcSTR['center'][0], slipArcSTR['center'][1], 'kx')
        # Plot the slip circular arc.
        plt.plot(arcPointsCoordsArray[:,0], arcPointsCoordsArray[:,1], 'k-', \
            lw=0.3)
        # Plot the slices.
        for i in range(len(slicesSTRCell)):
            plotslice(slicesSTRCell[i])
        # Plot the material boundary and the slope geometry.
        plt.plot(boundPointsCordsArray[:,0], boundPointsCordsArray[:,1], 'k-')
        # Plot the terrain surface.
        plt.plot(surfaceChordsArray[:,0], surfaceChordsArray[:,1], 'k', lw=2)
        # Plot the water table.
        plt.plot(wtCoordsArray[:,0], wtCoordsArray[:,1], 'b-')
        # Plot the radius of the arc at both ends.
        radius1PlotArray = np.vstack((slipArcSTR['center'], pointAtToeVec))
        plt.plot(radius1PlotArray[:,0], radius1PlotArray[:,1], 'k--', lw=0.5)
        radius2PlotArray = np.vstack((slipArcSTR['center'], pointAtCrownVec))
        plt.plot(radius2PlotArray[:,0], radius2PlotArray[:,1], 'k--', lw=0.5)
        # Plot the factor of safety value in graphic.
        if methodString == 'Allm':
            fsText = ' $f_{\mathrm{s}\, \mathrm{(Fellenius)}}=$'+\
                format(selectedFs[0], '.3f')+'\n'+\
                ' $f_{\mathrm{s}\, \mathrm{(Bishop\, Simp.)}}=$'+\
                format(selectedFs[1], '.3f')
        else:
            if methodString == 'Bshp':
                fsText = ' $f_{\mathrm{s}\, \mathrm{(Bishop\, Simp.)}}=$'+\
                    str(format(selectedFs, '.3f'))
            else: 
                fsText = ' $f_{\mathrm{s}\, \mathrm{(Fellenius)}}=$'+\
                    str(format(selectedFs, '.3f'))
        plt.text(0, surfaceChordsArray[0,1], fsText, fontsize = 11, \
            horizontalalignment='left', verticalalignment='bottom')
        ## Final plot details.
        plt.axis('equal')
        plt.xlabel('$x$ distance')
        plt.ylabel('$y$ distance')
        plt.title(projectName)
        # plt.hold(False)
        plt.savefig(projectName+outputFormatImg, dpi=300)
        
        #----------------------------------------------------------------------
        ## Exporting summary data
        outFile = open(projectName+'.txt', 'w')
        outFile.write(\
            '---SUMMARY OF PROJECT---\n \n'+\
            'Project name: '+projectName+'\n'+\
            'Author: '+projectAuthor+'\n'+\
            'Date: '+str(projectDate)+'\n'+\
            'Safety factors: \n'+\
            '    -Fellenius method: '+str(fsSatCell[0])+'\n'+\
            '    -Bishop method: '+str(fsSatCell[1])+'\n \n'+\
            '--Slope geometry--\n'+\
            'Height: '+str(slopeHeight[0])+' '+slopeHeight[1]+'\n'+\
            'Dip: '+str(np.degrees(np.tan(slopeDip[1]/slopeDip[0])))+\
                ' degrees\n'+\
            'Crown distance: '+str(crownDist[0])+' '+crownDist[1]+'\n'+\
            'Toe distance: '+str(toeDist[0])+' '+toeDist[1]+'\n'+\
            'Toe depth: '+str(toeDepth[0])+' '+toeDepth[1]+'\n'+\
            'Surface coordinates: \n'+str(surfaceChordsArray)+'\n \n'+\
            '--Watertable geometry--\n'+\
            'Depth at crown: '+str(wtDepthAtCrown[0])+' '+wtDepthAtCrown[1]+\
                '\n'+\
            'Is the slope partially submerged? '+slopeSubmergedAns+'\n'+\
            'Watertable coordinates: \n'+str(wtCoordsArray)+'\n \n'+\
            '--Slip circle--\n'+\
            'Radius: '+str(slipRadius[0])+' '+slipRadius[1]+'\n'+\
            'Center coordinates: '+str(slipArcSTR['center'])+'\n \n'+\
            '--Materials properties--\n'+\
            'Water unit weight: '+str(waterUnitWeight[0])+' '+\
                waterUnitWeight[1]+'\n'+\
            'Soil unit weight: '+str(materialUnitWeight[0])+' '+\
                materialUnitWeight[1]+'\n'+\
            'Friction angle '+str(frictionAngleGrad[0])+' '+\
                frictionAngleGrad[1]+'\n'+\
            'Cohesion: '+str(cohesion[0])+' '+cohesion[1]+'\n \n'+\
            '--Slices data--\n'+\
            'Number of slices: '+str(numSlices)+'\n'+\
            'Has the surface slip constant width slices? '+\
                constantSliceWidthAns+'\n \n'+\
            'Slices structures data: \n'+\
            str(reportCell)+'\n \n'+\
            'Note: This program calculated the safety factor to circular '+\
            'slip,\nunder limit equilibrium considerations, using '+\
            'Fellenius and Bishop \nmethods. The imagen attached shows the '+\
            'calculation performed.\n\n'+\
            'This program is distributed in the hope that it will be useful,'+\
            '\nbut WITHOUT ANY WARRANTY; without even the implied warranty '+\
            'of \nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.')
        outFile.close()
    return msg


get_fos = onlyonecircle

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
