# import modules
import matplotlib.pyplot as plt

'''
# Description.
Plot one slide from its structure.

# Input(s).
Slices dictionary type structures (slicesSTRCell). Has the following fields:
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

# Output(s).
Array containing the coordinates of the slice contourn
(slicePlineCordsArray).

# Example1.
slicesSTR = \
{'area': 18.063276613019383,
 'hrzMomentArm': -5.4527963142320601,
 'inclinationAngleGradAtBottom': 21.379968728885775,
 'inclinationAngleGradAtTop': 68.198590513648185,
 'midHeight': 8.6015602919139909,
 'midPoint': np.array([ 11.45      ,   3.07666551]),
 'plineCords': np.array([[ 10.4       ,  14.30322581],
        [ 10.4       ,   3.4877326 ],
        [ 11.45      ,   3.07666551],
        [ 12.5       ,   2.66559843],
        [ 12.5       ,   9.05322581],
        [ 10.4       ,  14.30322581]]),
 'vrtMomentArm': 5.3266677434544878,
 'width': 2.0999999999999996,
 'wtMidHeight': 8.6015602919139909,
 'wtMidHeightAboveSlope': 0.0}

---
slicePlineCordsArray = plotslice(slicesSTR)
'''
def plotslice(slicesSTR):   
    # plt.hold(True)
    #Plot the slice contourn and middle point
    plt.plot(slicesSTR['plineCords'][:,0], slicesSTR['plineCords']\
        [:,1], 'k-', lw=0.5)
    plt.plot(slicesSTR['midPoint'][0], slicesSTR['midPoint'][1], 'k.', lw=0.3)
    
    #redirecting the to the output variable
    slicePlineCordsArray = slicesSTR['plineCords']

    return slicePlineCordsArray
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
