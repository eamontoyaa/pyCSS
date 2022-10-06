'''
# Description.
This is the graphical user interface (GUI) module in order to perform a \
circular arc slope stability analysis by the limit equilibrium model by 
Fellenius and Bishop symplified methods implemented in pyCSS program.
'''

#------------------------------------------------------------------------------
## Add functions path
import sys
sys.path += ['./functions']

#------------------------------------------------------------------------------
## Modules/Functions import
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import numpy as np
import time

from automaticslipcircles import automaticslipcircles
from onlyonecircle import onlyonecircle

#####---------------------------------------------------------------------#####
## master window

gui = Tk()
gui.geometry("790x370")
gui.title('pyCSS')

#####---------------------------------------------------------------------#####
## Poject data ##
projectDataFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, \
    text='Información del proyecto', width=200, height=105).place(x=20, y=20)

Label(projectDataFrame, text='Título').place(x=30, y=40)
projectNameVal = StringVar() ##### projectName #####
Entry(projectDataFrame, width=15, textvariable=projectNameVal).place(x=84, \
    y=40)
    
Label(projectDataFrame, text='Autor').place(x=30, y=60)
projectAuthorVal = StringVar() ##### projectAuthor #####
Entry(projectDataFrame, width=15, textvariable=projectAuthorVal).place(x=84,\
    y=60)

def setwaterunitweight():
    if units.get() == 1:
        waterUnitWeightVal.set(9.81)
    elif units.get() == 2:
        waterUnitWeightVal.set(62.4)
Label(projectDataFrame, text='Unidades').place(x=30, y=90)
units = IntVar()##### units #####
Radiobutton(projectDataFrame, text='m - kN/m3 - kPa', value=1, \
    variable=units, command=setwaterunitweight).place(x=90, y=80)
Radiobutton(projectDataFrame, text='ft - pcf - psf', value=2, \
    variable=units, command=setwaterunitweight).place(x=90, y=97.5)
units.set(1)

#####---------------------------------------------------------------------#####
## slope geometry ##

geometrySlopeFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, width=200,\
    height=170, text='Geometría del talud').place(x=20, y=140)

Label(geometrySlopeFrame, text='Altura').place(x=30, y=160)
slopeHeightVal = DoubleVar() ##### slopeHeight #####
Entry(geometrySlopeFrame, width=8, textvariable=slopeHeightVal).place(x=140, \
    y=160)

Label(geometrySlopeFrame, text='Longitud corona').place(x=30, y=180)
crownDistVal = DoubleVar() #### crownDist #####
Entry(geometrySlopeFrame, width=8, textvariable=crownDistVal).place(x=140, \
    y=180)

Label(geometrySlopeFrame, text='Longitud pie').place(x=30, y=200)
toeDistVal = DoubleVar()  ##### toeDist #####
Entry(gui, width=8, textvariable=toeDistVal).place(x=140, \
    y=200)

Label(geometrySlopeFrame, text='Pendiente').place(x=30, y=230)
Label(geometrySlopeFrame, text=u'\u0394'+'x:', font='Verdana 8').\
    place(x=105, y=220)
slopeDip0 = DoubleVar() ##### slopeDip-0 #####
Entry(geometrySlopeFrame, width=8, textvariable=slopeDip0).place(x=140, \
    y=220)
Label(geometrySlopeFrame, text=u'\u0394'+'y:', font='Verdana 8').\
    place(x=105, y=240)
slopeDip1 = DoubleVar() ##### slopeDip-1 #####
Entry(geometrySlopeFrame, width=8, textvariable=slopeDip1).place(x=140, \
    y=240)

Label(geometrySlopeFrame, text='Profundidad').place(x=30, y=260)
toeDepthVal = DoubleVar() ##### toeDepth #####
Entry(geometrySlopeFrame, width=8, textvariable=toeDepthVal, \
        state='normal').place(x=140, y=260)
def toeDepthValActivate():
    if wantAutomaticToeDepthVal.get() == True:
        Entry(geometrySlopeFrame, width=8, textvariable=toeDepthVal, \
        state='disabled').place(x=140, y=260)
    else:
        Entry(geometrySlopeFrame, width=8, textvariable=toeDepthVal, \
        state='normal').place(x=140, y=260)
wantAutomaticToeDepthVal = BooleanVar() ##### wantAutomaticToeDepth #####
Checkbutton(geometrySlopeFrame, text='Profundidad automática', \
    variable=wantAutomaticToeDepthVal, onvalue=True, offvalue=False, \
    command=toeDepthValActivate).place(x=40, y=280)

#####---------------------------------------------------------------------#####
## Slip arc-circle ##

# only one circle 
slipCircleFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, width=540, \
    height=125, text='Superficie circular').place(x=230,y=20)

wantEvaluateOnlyOneSurfaceVal = BooleanVar() ### wantEvaluateOnlyOneSurface ###
wantEvaluateOnlyOneSurfaceVal.set(True)
def wantEvaluateOnlyOneSurfaceActivate():
    if wantEvaluateOnlyOneSurfaceVal.get() == True:
        Entry(slipCircleFrame, width=8, textvariable=\
            hztDistPointAtCrownFromCrownVal, state='normal').place(x=366, y=60)
        Entry(slipCircleFrame, width=8, \
            textvariable=hztDistPointAtToeFromCrownVal, state='normal').place(\
            x=366, y=80)
        Entry(slipCircleFrame, width=8, textvariable=slipRadiusVal, \
            state='normal').place(x=366, y=100) ###---
        Entry(slipCircleFrame, width=8, textvariable=numCirclesVal, \
            state='disabled').place(x=690, y=40)
        Entry(slipCircleFrame, width=8, textvariable=radiusIncrementVal, \
            state='disabled').place(x=690, y=60)
        Entry(slipCircleFrame, width=8, textvariable=numberIncrementsVal, \
            state='disabled').place(x=690, y=80)
        Entry(slipCircleFrame, width=8, textvariable=maxFsValueContVal, \
            state='disabled').place(x=690, y=100) ###---
        ttk.Combobox(values=['Fellenius', 'Bishop', 'Ambos'], state='normal',\
            textvariable=methodStringVal, width=7).place(x=420, y=300)  
    else:
        Entry(slipCircleFrame, width=8, textvariable=\
            hztDistPointAtCrownFromCrownVal, state='disabled').place(\
            x=366, y=60)
        Entry(slipCircleFrame, width=8, \
            textvariable=hztDistPointAtToeFromCrownVal, state='disabled').\
            place(x=366, y=80)
        Entry(slipCircleFrame, width=8, textvariable=slipRadiusVal, \
            state='disabled').place(x=366, y=100) ###---        
        Entry(slipCircleFrame, width=8, textvariable=numCirclesVal, \
            state='normal').place(x=690, y=40)
        Entry(slipCircleFrame, width=8, textvariable=radiusIncrementVal, \
            state='normal').place(x=690, y=60)
        Entry(slipCircleFrame, width=8, textvariable=numberIncrementsVal, \
            state='normal').place(x=690, y=80)
        Entry(slipCircleFrame, width=8, textvariable=maxFsValueContVal, \
            state='normal').place(x=690, y=100) ###---
        methodStringVal.set('Ambos')
        ttk.Combobox(values=['Fellenius', 'Bishop', 'Ambos'], state='disable',\
            textvariable=methodStringVal, width=7).place(x=420, y=300)      
Checkbutton(slipCircleFrame, text='Evaluar una única superficie', \
    variable=wantEvaluateOnlyOneSurfaceVal, onvalue=True, offvalue=False, \
    command=wantEvaluateOnlyOneSurfaceActivate).place(x=235, y=40)

Label(slipCircleFrame, text='Primer punto*').place(x=240, y=60)
hztDistPointAtCrownFromCrownVal = DoubleVar() ## hztDistPointAtCrownFromCrown #
Entry(slipCircleFrame, width=8, textvariable=hztDistPointAtCrownFromCrownVal)\
    .place(x=366, y=60)
    
Label(slipCircleFrame, text='Segundo punto*').place(x=240, y=80)
hztDistPointAtToeFromCrownVal = DoubleVar() ## hztDistPointAtToeFromCrownVal ##
Entry(slipCircleFrame, width=8, textvariable=hztDistPointAtToeFromCrownVal)\
    .place(x=366, y=80)

Label(slipCircleFrame, text='Radio').place(x=240, y=100)
slipRadiusVal = DoubleVar() ##### slipRadius #####
Entry(slipCircleFrame, width=8, textvariable=slipRadiusVal)\
    .place(x=366, y=100)

Label(slipCircleFrame, text='* Medida horizontal desde el vértice de la '+ 
    'corona. Valores a la izquierda del vértice son negativos y a la '+
    'derecha positivos.', justify='left', font='Arial 7').place(x=240, y=120)

# multiple circles
Label(slipCircleFrame, text='Número de superficies consideradas').\
    place(x=460, y=40)
numCirclesVal = DoubleVar() ##### numCircles #####
Entry(slipCircleFrame, width=8, textvariable=numCirclesVal, state='disabled'\
    ).place(x=690, y=40)
numCirclesVal.set(500)

Label(slipCircleFrame, text='Longitud que aumenta el radio').place(x=460, y=60)
radiusIncrementVal = DoubleVar() ##### radiusIncrement #####
Entry(slipCircleFrame, width=8, textvariable=radiusIncrementVal, \
    state='disabled').place(x=690, y=60)
radiusIncrementVal.set(3)

Label(slipCircleFrame, text='Cantidad de incrementos en el radio').\
    place(x=460, y=80)
numberIncrementsVal = DoubleVar() ##### numberIncrements #####
Entry(slipCircleFrame, width=8, textvariable=numberIncrementsVal, \
    state='disabled').place(x=690, y=80)
numberIncrementsVal.set(4)

Label(slipCircleFrame, text='Máximo valor de Fs para mostrar', justify='left')\
    .place(x=460, y=100)
maxFsValueContVal = DoubleVar() ##### maxFsValueCont #####
Entry(slipCircleFrame, width=8, textvariable=maxFsValueContVal, \
    state='disabled').place(x=690, y=100)
maxFsValueContVal.set(3)

#####---------------------------------------------------------------------#####
## watertable surface ##    

watertableFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, width=270, \
    height=90, text='Nivel freático').place(x=230, y=150)

Label(watertableFrame, text='Profundidad desde la corona').place(\
    x=240, y=190)
wtDepthAtCrownVal = DoubleVar() ##### wtDepthAtCrown #####
Entry(watertableFrame, width=8, textvariable=wtDepthAtCrownVal).place(x=420, \
    y=190)

toeUnderWatertableVal = BooleanVar() ##### toeUnderWatertable #####
Checkbutton(watertableFrame, text='Talud parcialmente sumergido', \
    variable=toeUnderWatertableVal, onvalue=True, offvalue=False).place(\
    x=235, y=210)

wantWatertableVal = BooleanVar() ##### wantWatertable #####
wantWatertableVal.set(True)
def wantWatertableActivate():
    if wantWatertableVal.get() == True:
        Entry(watertableFrame, width=8, textvariable=wtDepthAtCrownVal, \
            state='normal').place(x=420, y=190)
        Checkbutton(watertableFrame, text='Talud parcialmente sumergido', \
            variable=toeUnderWatertableVal, onvalue=True, offvalue=False, \
            state='normal').place(x=235, y=210)
    else:
        Entry(watertableFrame, width=8, textvariable=wtDepthAtCrownVal, \
            state='disabled').place(x=420, y=190)
        Checkbutton(watertableFrame, text='Talud parcialmente sumergido', \
            variable=toeUnderWatertableVal, onvalue=True, offvalue=False, \
            state='disabled').place(x=235, y=210)
Checkbutton(watertableFrame, text='Incluir nivel freático', \
    variable=wantWatertableVal, onvalue=True, offvalue=False, \
    command=wantWatertableActivate).place(x=235, y=170)
    
#####---------------------------------------------------------------------#####
## Material properties ##    

watertableFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, width=260, \
    height=115, text='Propiedades de los materiales').place(x=510, y=150)

Label(watertableFrame, text='Peso específico del agua').place(\
    x=520, y=170)
waterUnitWeightVal = DoubleVar() ##### waterUnitWeight #####
Entry(watertableFrame, width=8, textvariable=waterUnitWeightVal).place(x=690, \
    y=170)
waterUnitWeightVal.set(9.81)

Label(watertableFrame, text='Peso específico del suelo').place(\
    x=520, y=190)
materialUnitWeightVal = DoubleVar() ##### materialUnitWeight #####
Entry(watertableFrame, width=8, textvariable=materialUnitWeightVal).place(\
    x=690, y=190)

Label(watertableFrame, text='Ángulo de fricción del suelo').place(\
    x=520, y=210)
frictionAngleGradVal = DoubleVar() ##### frictionAngleGrad #####
Entry(watertableFrame, width=8, textvariable=frictionAngleGradVal).place(\
    x=690, y=210)

Label(watertableFrame, text='Cohesión del suelo').place(\
    x=520, y=230)
cohesionVal = DoubleVar() ##### cohesion #####
Entry(watertableFrame, width=8, textvariable=cohesionVal).place(\
    x=690, y=230)

#####---------------------------------------------------------------------#####
## Advanced variables ##    

watertableFrame = LabelFrame(gui, relief=RIDGE, borderwidth=1.5, width=270, \
    height=110, text='Variables avanzadas').place(x=230, y=240)

Label(watertableFrame, text='Número de dovelas').place(x=240, y=260)
numSlicesVal = IntVar() ##### numSlices #####
Spinbox(watertableFrame, from_=2, to=50, width=7, textvariable=numSlicesVal).\
    place(x=420, y=260)
numSlicesVal.set(10)

wantConstSliceWidthTrueVal = BooleanVar() ##### wantConstSliceWidthTrue #####
Checkbutton(watertableFrame, text='Ancho de las dovelas constante', \
    variable=wantConstSliceWidthTrueVal, onvalue=True, offvalue=False).place(\
    x=240, y=280)
wantConstSliceWidthTrueVal.set(True)

Label(watertableFrame, text='Método de análisis').place(x=240, y=300)
methodStringVal = StringVar() ##### methodString #####
ttk.Combobox(values=['Fellenius', 'Bishop', 'Ambos'],\
    textvariable=methodStringVal, width=7).place(x=420, y=300)
methodStringVal.set('Bishop')

Label(watertableFrame, text='Formato de la imágen').place(x=240, y=320)
outputFormatImgVal = StringVar() ##### outputFormatImg #####
outputFormatImgList = ['.eps', '.jpeg', '.jpg', '.pdf', '.pgf', '.png', '.ps',\
    '.raw', '.rgba', '.svg', '.svgz', '.tif', '.tiff']
ttk.Combobox(values=outputFormatImgList, textvariable=outputFormatImgVal, \
    width=7).place(x=420, y=320)
outputFormatImgVal.set('.svg')

def exitgui():
    return gui.quit()
#gui.destroy(), 
def cssanalysis():
    ## Units  
    unitTemp = units.get()
    if unitTemp == 1:
        unitsTuple = ('m', 'kN/m3', 'kPa')
    else:
        unitsTuple = ('ft', 'pcf', 'psf')
    ## Poject data
    projectName = projectNameVal.get()
    projectAuthor = projectAuthorVal.get()
    projectDate = time.strftime("%d/%m/%y")
    ## The slope geometry
    slopeHeight = [slopeHeightVal.get(), unitsTuple[0]]
    crownDist = [crownDistVal.get(), unitsTuple[0]]
    toeDist = [toeDistVal.get(), unitsTuple[0]]
    slopeDip = np.array([slopeDip0.get(), slopeDip1.get()])
    toeDepth = [toeDepthVal.get(), unitsTuple[0]]
    wantAutomaticToeDepth = wantAutomaticToeDepthVal.get()
    # The slip arc-circle
    wantEvaluateOnlyOneSurface = wantEvaluateOnlyOneSurfaceVal.get()
    hztDistPointAtCrownFromCrown = [hztDistPointAtCrownFromCrownVal.get(),\
        unitsTuple[0]]
    hztDistPointAtToeFromCrown = [hztDistPointAtToeFromCrownVal.get(),\
        unitsTuple[0]]
    slipRadius = [slipRadiusVal.get(), unitsTuple[0]]
    numCircles = int(numCirclesVal.get())
    radiusIncrement = [radiusIncrementVal.get(), unitsTuple[0]]
    numberIncrements = int(numberIncrementsVal.get())
    maxFsValueCont = maxFsValueContVal.get()
    # Watertable
    wtDepthAtCrown = [wtDepthAtCrownVal.get(), unitsTuple[0]]
    toeUnderWatertable = toeUnderWatertableVal.get()
    wantWatertable = wantWatertableVal.get()
    # Materials properties.
    waterUnitWeight = [waterUnitWeightVal.get(), unitsTuple[1]]
    materialUnitWeight = [materialUnitWeightVal.get(), unitsTuple[1]]
    frictionAngleGrad = [frictionAngleGradVal.get(), 'degrees']
    cohesion = [cohesionVal.get(), unitsTuple[2]]
    # Advanced inputs
    numSlices = numSlicesVal.get()
    nDivs = numSlices
    wantConstSliceWidthTrue = wantConstSliceWidthTrueVal.get()
    if methodStringVal.get() == 'Fellenius':
        methodString = 'Flns'
    elif methodStringVal.get() == 'Bishop':
        methodString = 'Bshp'
    else:
        methodString = 'Allm'
    outputFormatImg = outputFormatImgVal.get()
    
    #--------------------------------------------------------------------------
    # Operations for only one slip surface
    if wantEvaluateOnlyOneSurface == True:
        msg = onlyonecircle(projectName, projectAuthor, projectDate, \
            slopeHeight, slopeDip, crownDist, toeDist, wantAutomaticToeDepth, \
            toeDepth,hztDistPointAtCrownFromCrown, hztDistPointAtToeFromCrown,\
            slipRadius, wantWatertable, wtDepthAtCrown, toeUnderWatertable, \
            waterUnitWeight, materialUnitWeight, frictionAngleGrad, cohesion, \
            wantConstSliceWidthTrue, numSlices, nDivs, methodString, \
            outputFormatImg)
        messagebox.showinfo(title='pyCSS', message=msg)
        anotherAnalysis = messagebox.askyesno(title='pyCSS', message='¿Desea'+\
            ' realizar otro análisis?')

    #--------------------------------------------------------------------------
    # Operations for multiple slip surface   
    else:
        automaticslipcircles(projectName, projectAuthor, projectDate, \
            slopeHeight, slopeDip, crownDist, toeDist, wantAutomaticToeDepth, \
            toeDepth, numCircles, radiusIncrement, numberIncrements, \
            maxFsValueCont, wantWatertable, wtDepthAtCrown, \
            toeUnderWatertable, waterUnitWeight, materialUnitWeight, \
            frictionAngleGrad, cohesion, wantConstSliceWidthTrue, numSlices, \
            nDivs, methodString, outputFormatImg)
        messagebox.showinfo(title='pyCSS', \
            message='Analysis successfully!')
        anotherAnalysis = messagebox.askyesno(title='pyCSS', message='¿Desea'+\
            ' realizar otro análisis?')
    
    if anotherAnalysis == False:
        exitgui() ##### close GUI #####

cssanalysisButton = Button(gui, text='Ejecutar análisis', command=cssanalysis,\
    height=1, width=29).place(x=510, y=280)

exitButton = Button(gui, text='Salir', command=exitgui,\
    height=1, width=29).place(x=510, y=320)

gui.mainloop()
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
