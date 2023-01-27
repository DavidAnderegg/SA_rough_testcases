from adflow_util import ADFLOW_UTIL
import argparse
import os
import numpy as np


defaultFuncList = [
    "lift",
    "drag",
    "cl",
    "cd",
    "fx",
    "fy",
    "fz",
    "cfx",
    "cfy",
    "cfz",
    "mx",
    "my",
    "mz",
    "cmx",
    "cmy",
    "cmz",
    "sepsensor",
    "sepsensoravgx",
    "sepsensoravgy",
    "sepsensoravgz",
]

options = {
    'name': "mdo_tutorial",
    'autoRestart': False,
    'surfaceFamilyGroups': {
        "wing": ["wall", "le"]
    },
    #'useComplexADflow': True,
}

aeroOptions = {
        'alpha': 1.8,
        'mach': 0.80,
        'P': 20000.0,
        'T': 220.0,
        'areaRef':45.5,
        'chordRef':3.25,
        'beta':0.0,
        'R':287.87,
        'xRef':0.0,
        'yRef':0.0,
        'zRef':0.0,
        'evalFuncs':defaultFuncList,
}

solverOptions = {
    # Common Parameters
    'gridFile': 'mdo_tutorial_rough.cgns',
    #'restartFile': 'output/mdo_tutorial_vol.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useBlockettes': False,
    'useRoughSA': True, 


    # "MGCycle": "2w",
    # "equationType": "RANS",
    # "smoother": "DADI",
    # "CFL": 1.25,
    # "CFLCoarse": 1.25,
    # "resAveraging": "never",
    "nSubiter": 3,
    "nSubiterTurb": 3,
    "nCyclesCoarse": 100,
    "nCycles": 1000,
    "monitorVariables": ["resrho", "totalr", "cl", "cd"],
    # "volumeVariables": ["resrho", "ks"],
    "useNKsolver": True,
    # "ANKSwitchTol": 1e-2,
    "ANKSecondordSwitchTol": 1e-2,
    "L2Convergence": 1e-15,
    "NKSwitchTol": 1e-5,
    "adjointL2Convergence": 1e-16,
    "blockSplitting": True,
    "NKjacobianlag": 2,

    "solutionPrecision": "double",
    "outputSurfaceFamily": "wing",
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
