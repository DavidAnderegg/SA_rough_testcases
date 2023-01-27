from adflow_util import ADFLOW_UTIL
import argparse
import os
import numpy as np



parser = argparse.ArgumentParser(
    description='.'
)
parser.add_argument('-face', type=str, default=None,
                    help='.')

args = parser.parse_args()


if args.face is None:
    faces = ['kLow', 'kHigh', 'jLow', 'jHigh', 'iLow', 'iHigh']
else:
    faces = [args.face]


for face in faces:
    options = {
        'name': f'cuboid_{face}',
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
        'gridFile': os.path.join('meshes', f'cuboid_{face}.cgns'),
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
        'volumevariables': ['resrho', 'ks', 'dist'],
        'solutionPrecision': 'double',
        'solutionPrecisionSurface': 'double',
        'gridPrecisionSurface': 'double',
        'nCycles':1,
        'L2Convergence':1e-12,
    }

    au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
    au.run()
