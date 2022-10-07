Circular Slope Stability PyProgram (pyCSS)
==========================================

It is an open-source program written in Python for 2D slope stability analysis of circular surfaces by the limit equilibrium method (Fellenius and Bishop methods).

.. image:: https://raw.githubusercontent.com/eamontoyaa/pyCSS/master/other_files/figures/output_example_Fs.svg
  :width: 500
  :alt: Assessment of a single potential circular failure surface

.. image:: https://raw.githubusercontent.com/eamontoyaa/pyCSS/master/other_files/figures/output_example_Fs-min.svg
  :width: 500
  :alt: Assessment of a multiple potential circular failure surface for getting the minimum Fs

Downloading the program
-----------------------

To install **pyCSS v0.1.0** from PyPI, run this command in your terminal:

.. code-block:: console

    pip install pycss-lem

Also, you can clone the original repo directory (release v0.0.9) using git:

.. code-block:: console

    git clone https://github.com/eamontoyaa/pyCSS/ --branch v0.0.9

or directly use the download options from GitHub.

Installing dependencies
-----------------------

The program has been tested in Python ≥3.6.  It is suggested to create a virtual environment to use the program.

From release v0.1.0, the program is expected to install its dependencies automatically. If this does not happen, please follow the instructions as for previous releases:

Download the `requirements.txt` file. In the same directory, type and execute the following line in your terminal:

.. code-block:: console

    python3 -m pip install -r requirements.txt

Usage
-----

Release v0.1.0+
^^^^^^^^^^^^^^^

Please, refer to `this notebook <https://github.com/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/limit_equilibrium_method.ipynb>`_ prepared
for the Slope Stability class at EAFIT University (Colombia).  There, you will find a series of commented code blocks to carry out a stability assessment
using **pyCSS**.

You can run the program by editing the `script_template.py` file located in the `./examples/` directory of the installation folder.
Use the examples located in the same folder as an input guide.
Then, save the script wherever you need it to be saved, and run it by typing the following line from the terminal:

.. code-block:: console

    python3 script_template.py

**Note:** the graphical user interface is not yet available from release v0.1.0.


Release v0.0.9
^^^^^^^^^^^^^^

You can run the program via GUI by typing the following line in the root directory:

.. code-block:: console

    python3 pyCSS.py

Or editing the `finalModule.py` file located in the root directory and running it:

.. code-block:: console

    python3 finalModule.py

You can test the program by runing the files in the `/examples` folder.

.. code-block:: console

    cd examples/
    python3 example01.py


If the example runs successfully, the program will create two files. One is a graphical output of the slope and the stability analysis. The second file is a text file with a summary of the run.


Documentation
-------------

Please refer to the user manual `user manual for release v0.0.9 <https://github.com/eamontoyaa/pyCSS/blob/master/other_files/pyCSSmanualSpanish.pdf>`_ to learn more. Currently, the manual is in Spanish, but in the future, we will translate it to English.

Citation
--------

To cite **pyCSS** in publications, use:

    Suarez-Burgoa, Ludger O., and Exneyder A. Montoya-Araque. 2016.
    “Programa en código abierto para el análisis bidimensional de estabilidad
    de taludes por el método de equilibrio límite.” Revista de La Facultad
    de Ciencias 5 (2): 88–104. <https://doi.org/10.15446/rev.fac.cienc.v5n2.59914>.

A BibTeX entry for LaTeX users is:

.. code:: bibtex

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

