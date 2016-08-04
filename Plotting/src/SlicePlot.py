#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os
import pickle
from math import sqrt, exp,log
from array import array


########################################
# Class
########################################

class SlicePlot:

    def __init__( self, name=None, longname=None, plotdir='plots' ):
        
        if not name:
            self.name = 'TODO'
        else:
            self.name = name

        if not longname:
            self.longname = 'TODO'
        else:
            self.longname = longname

        self.plotdir   = plotdir
        self.pickledir = 'FitPickles'


        self.sliceplot_y_min = 0.95
        self.sliceplot_y_max = 1.03

        self.sliceplotsigma_y_min   = 0.0
        self.sliceplotsigma_y_max   = 0.1

        self.sliceplot_legheight    = 0.12

        self.sliceplot_LeftMargin   = 0.14 
        self.sliceplot_RightMargin  = 0.04 
        self.sliceplot_BottomMargin = 0.14 
        self.sliceplot_TopMargin    = 0.01 + self.sliceplot_legheight

        self.sliceplot_cwidth       = 1000
        self.sliceplot_cheight      = 800


        self.perbin_cwidth          = 1000
        self.perbin_cheight         = 1000

        self.fit_x_min = 0.8
        self.fit_x_max = 1.1

        self.Verbosity = 10

        self.colorlist = [ 2, 3, 4, 6, 8, 9, 30, 40, 41, 43, 46 ]


    def SetDataset( self, hdata ):
        self.hdata = hdata

    def SetHistVars( self, histvars ):
        self.histvars = histvars

    def SetSliceVar( self, slicevar, bounds ):
        self.slicevar = slicevar
        self.slicevarname = slicevar.GetName()
        self.bounds = bounds
        self.n_bins = len(bounds) - 1
        if self.name == 'TODO':
            self.name = self.slicevarname
            self.longname = self.name

    def p( self, text, verbosity=2 ):
        if verbosity <= self.Verbosity:
            print '  '*verbosity + text

    # Save a canvas
    def Save( self, canvas, filename ):
        outputname = os.path.join( self.plotdir, self.name + '_' + filename )
        self.p( 'Saving canvas with filename ' + outputname, 2 )
        canvas.SaveAs( outputname + '.pdf' )

# Set class methods from other modules

from SlicePlot_fitting import *
SlicePlot.FitSlices = FitSlices
SlicePlot.FitOneSlice = FitOneSlice

from SlicePlot_plotting import *
SlicePlot.MakePlots_standard = MakePlots_standard

from SlicePlot_compareTRK import *
SlicePlot.MakePlots_comparison = MakePlots_comparison


