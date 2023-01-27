from adflow_util import ADFLOW_UTIL
import argparse
import os
import numpy as np


def preRunCallBack(solver, ap, n):

    # "Pressure", "PressureStagnation", "Temperature", "TemperatureStagnation", "Thrust", "Heat"

#    ap.setBCVar("SandGrainRoughness", 1e-3, 'rough')
    pass



options = {
    'name': f'cube_overset',
#    'preRunCallBack':  preRunCallBack,
    'autoRestart': False,
}

aeroOptions = {
    'alpha': 0,
    'T': 300, # 540 rankine
    'P': 1013e2,
    'V': 78.554,

    'areaRef': 2.0,
    'chordRef': 2.0,
    'evalFuncs': ['forcexpressure', 'forcexviscous', 'forcexmomentum', 'cd'],
}

solverOptions = {
    # Common Parameters
    'gridFile': 'cube.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useBlockettes': False,
    'useRoughSA': True, 

    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd'],
    'printIterations': True,
    'writeSurfaceSolution': True, 
    'writeVolumeSolution': True,
#    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cf', 'ch', 'cp'],
    'volumevariables': ['resrho', 'ks', 'dist', 'blank'],
    'solutionPrecision': 'double',
    'solutionPrecisionSurface': 'double',
    'gridPrecisionSurface': 'double',
    'nCycles':1,
    'L2Convergence':1e-12,
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
