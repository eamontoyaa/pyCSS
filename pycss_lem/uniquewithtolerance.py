# import modules
import numpy as np

'''
# Description.
Given an array of two columns (n x 2), the function extracts unique row
values that are not necessarily and strictly equal among other rows; the
desition is governed by a tolerance value.

# Input(s).
Array of n x 2 of dimension (array).

Number that will define the tolerance of the selection criterium (tolerance).

# Output(s).
New array with unique rows (uniqueArray).

# Example:
Given the following array:
array = np.array([\
   [ 9.   ,  2.   ],
   [ 7.   ,  4.123],
   [ 5.   ,  6.129],
   [ 7.   ,  8.12 ],
   [ 0.   ,  1.1  ],
   [ 9.001,  2.   ]])
it's obtained:
array([[ 0.   ,  1.1  ],
       [ 5.   ,  6.129],
       [ 7.   ,  4.123],
       [ 7.   ,  8.12 ],
       [ 9.   ,  2.   ]])
---
uniqueArray = uniquewithtolerance(array, tolerance = 0.001)
'''
def uniquewithtolerance( array, tolerance = 0.001):

    ## Doing the sort
    indexes = np.argsort(array, 0)
    sortedArray = array[indexes[:,0], :]
    
    ## Applying the tolerance criterium
    uniMaskX = np.diff(np.hstack((np.zeros(1), sortedArray[:,0]))) > tolerance
    uniMaskY = np.diff(np.hstack((np.zeros(1), sortedArray[:,1]))) > tolerance
    
    uniMask = np.logical_or(uniMaskX, uniMaskY)
    uniqueArray = sortedArray[uniMask,:] 
    
    return uniqueArray
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
