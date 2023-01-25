from adflow_util import ADFLOW_UTIL
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-level', type=int, default=4,
                help='The mesh level to revine')
parser.add_argument('-ks', type=float, default=0.0,
                    help='Equivalen sand-grain roughness')
args = parser.parse_args()

def preRunCallBack(solver, ap, n):

    # possible values are:
    # "Pressure", "PressureStagnation", "Temperature", "TemperatureStagnation", "Thrust", "Heat"
    ap.setBCVar("Pressure", 1013e2, "out")

    solver.setSurfaceRoughness(args.ks, 'wall')

# 4.5e6 -> 2060.5e2

if args.ks == 0:
    finish = 'clean'
else:
    finish = f'ks{args.ks:.3e}'
options = {
    'name': f'flatplate_blanchard_{finish}_L{args.level}',
    'preRunCallBack':  preRunCallBack,
    'autoRestart': False,
}

aeroOptions = {
    'alpha': 0,
    'T': 288,
    'P': 1013e2,
    'V': 45,

    'areaRef': 2.0,
    'chordRef': 2.0,
    'evalFuncs': ['forcexpressure', 'forcexviscous', 'forcexmomentum', 'cd'],
}

solverOptions = {
    # Common Parameters
    'gridFile': os.path.join('..', 'grids', f'flatplate_L{args.level}.cgns'),
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useBlockettes': False,
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
    'ankcoupledswitchtol': 1e-4,

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
