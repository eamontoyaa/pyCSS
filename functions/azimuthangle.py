# import modules
import numpy as np

'''
# Description.
Given a 2x1 vector, this function obtains the angle of the azimuth from
x-axis in a counter clockwise sense.
Coordiante system is with x in the abscisas and y in the ordinates  (i.e. 
x horizontal pointing to the right and y vertical pointing upwards).

# Input(s).
Array that representing a bi-dimensional vector (vector).

# Output(s).
Angle in radians representing the azimut of the vector (angleRad).
 
Example: giving next array
vector = np.array([3,-5]), is obtined  5.2528 radians
---
angleRad = azimuthangle(vector)
'''
def azimuthangle(vector):
    if vector[0] == 0:
        if vector[1] >= 0:
            angleRad = np.pi/2
        else:
            angleRad = 3*np.pi/2
    else:
        basicAngleRad = np.arctan(np.abs(vector[1])/np.abs(vector[0]))
        if vector[0] >= 0:
            if vector[1] >= 0: #case 1
                angleRad = basicAngleRad
            elif vector[1] < 0: #case 4
                angleRad = 2*np.pi-basicAngleRad
        elif vector[0] < 0:
            if vector[1] >= 0: #case 2
                angleRad = np.pi-basicAngleRad
            elif vector[1] < 0: #case 3
                angleRad = np.pi+basicAngleRad
        else:
            print("Error: bad number")

    return angleRad
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
