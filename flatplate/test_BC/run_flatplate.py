from adflow_util import ADFLOW_UTIL
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-level', type=int, default=4,
                help='The mesh level to revine')
parser.add_argument('-finish', type=str, default='clean')
args = parser.parse_args()


def preRunCallBack(solver, ap, n):

    # possible values are:
    # "Pressure", "PressureStagnation", "Temperature", "TemperatureStagnation", "Thrust", "Heat"
    ap.setBCVar("Pressure", 1000e2, "out")

    # set ks-values
    ks = np.zeros(28)
    if args.finish == 'last1_ks1.0e-03':
        ks[-1] = 1.0e-3
    if args.finish == 'last10_ks1.0e-03':
        ks[-10:] = 1.0e-3
    print(ks)
    walls = []
    for n in range(10, 28):
        wall = f"wall{n+1}"
        if ks[n] > 0:
            ap.setBCVar("SandGrainRoughness", ks[n], wall)
        walls.append(wall)

    # combine all walls to wall
    solver.addFamilyGroup('wall', walls)



options = {
    'name': f'flatplate_test_BC_{args.finish}_L{args.level}',
    'preRunCallBack':  preRunCallBack,
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
    'gridFile': f'input/flatplate_split_L{args.level}.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useBlockettes': False,
    # 'kssa': 1e-4,
    'useRoughSA': True,

    # SA model parameters
    # gives the default noft2 variant:
    "eddyvisinfratio": 0.210438,
    "useft2SA": False,
    "turbulenceproduction": "vorticity",

    # ANK
    'useanksolver': True,
    'anksecondordswitchtol': 1e-3,
    'ANKUnsteadyLSTol': 1.2,
    'ANKADPC': True,
    'ANKASMOverlap': 2,
    'ANKPCILUFill': 3,
    'ANKInnerPreconIts': 2,
    'ANKOuterPreconIts': 2,
    'ankcoupledswitchtol': 5e-5,

    # NK
    'useNKSolver':True,
    'nkswitchtol':1e-8,
    'NKADPC': True,
    'NKASMOverlap': 2,
    'NKPCILUFill': 3,
    'NKInnerPreconIts': 2,
    'NKOuterPreconIts': 2,

    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cf', 'ch', 'cp'],
    'volumevariables': ['resrho'],
    'solutionPrecision': 'double',
    'solutionPrecisionSurface': 'double',
    'gridPrecisionSurface': 'double',
    'nCycles':20000,
    'L2Convergence':1e-12,
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
