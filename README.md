# Circular Slope Stability PyProgram (pyCSS)

It is an open-source program written in Python for 2D slope stability analysis of circular surfaces by the limit equilibrium method (Fellenius and Bishop's method.

## Downloading the program

You can clone the repo using git:

    git clone https://github.com/eamontoyaa/pyCSS

or directly use the download option from GitHub.

## Installing dependencies

The program has been tested in Python ≥3.6.  It is suggested to create a virtual environment to use the program.

The dependencies can be installed by executing the following line:

    python3 -m pip install -r requirements.txt

## Usage

You can run the program via GUI by typing the following line in the root directory:

    python3 pyCSS.py

Or editing the `finalModule.py` file located in the root directory and running it:

    python3 finalModule.py

You can test the program by runing the files in the [example](./examples) folder.

``` bash
cd examples/
python3 example01.py
```

If the example runs successfully, the program will create two files. One is a graphical output of the slope and the stability analysis. The second file is a text file with a summary of the run.

Please refer to the user manual [user manual](files/pyCSSmanualSpanish.pdf) to learn more. Currently, the manual is in Spanish, but in the future, we will translate it to English.

Citation
--------

To cite **pyCSS** in publications, use:

    Suarez-Burgoa, Ludger O., and Exneyder Andrés Montoya-Araque. 2016. “Programa en código abierto para el análisis bidimensional de estabilidad de taludes por el método de equilibrio límite.” Revista de La Facultad de Ciencias 5 (2): 88–104. https://doi.org/10.15446/rev.fac.cienc.v5n2.59914.

A BibTeX entry for LaTeX users is:

``` bibtex
@article{SuarezBurgoa_MontoyaAraque_2016_art,
doi = {10.15446/rev.fac.cienc.v5n2.59914},
journal = {Revista de la Facultad de Ciencias},
keywords = {C{\'{o}}digo fuente libre,an{\'{a}}lisis de estabilidad de taludes,m{\'{e}}todo de Bishop,m{\'{e}}todo de equilibrio l{\'{i}}mite},
month = {jul},
number = {2},
pages = {88--104},
title = {{Programa en c{\'{o}}digo abierto para el an{\'{a}}lisis bidimensional de estabilidad de taludes por el m{\'{e}}todo de equilibrio l{\'{i}}mite}},
volume = {5},
year = {2016}
}
```
