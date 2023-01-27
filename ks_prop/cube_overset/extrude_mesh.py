import numpy as np
from scipy.spatial.transform import Rotation as R
from pyhyp import pyHyp
from cgnsutilities.cgnsutilities import Grid, readGrid, combineGrids, simpleCart
from idwarp import USMesh


ks_rough = 1.0
ks_clean = 0.1

# prepare bc-file
wall_str = '{i} kLow bcwall {family} BCDataSet_1 BCWall Dirichlet SandGrainRoughness {ks}\n'
bc_file_str = ''
families = {}
for i in range(1, 7):
    families[i] = 'rough'
    bc_file_str += wall_str.format(i=i, family=families[i], ks=ks_rough)

for i in range(7, 31):
    families[i] = 'clean'
    bc_file_str += wall_str.format(i=i, family=families[i],  ks=ks_clean)


options = {
    # ---------------------------
    #        Input Parameters
    # ---------------------------
    "fileType": 'CGNS',
    "inputFile": 'cube_surf.cgns',
    "unattachedEdgesAreSymmetry": False,
    "outerFaceBC": "overset",
    "autoConnect": True,
    # "BC": {1: {"jLow": "zSymm", "jHigh": "zSymm"}},
    "families": families,
    # ---------------------------
    #        Grid Parameters
    # ---------------------------
    "N": 20,
    "s0": 5e-1,
    "marchDist": 15.0,


    "epsE": 0.5,
    "epsI": 1.0,
    "theta": 0.0,
}


hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS("cube_vol.cgns")




ext = 12
overset = simpleCart(
        xMin=[-ext, -ext, -ext],
        xMax=[ext, ext, ext],
        dh=0.4,
        hExtra=0,
        nExtra=0,
        sym=[],
        mgcycle=1,
        outFile='cube_xoverset.cgns'
        )


# refine cube grid
cube = readGrid('cube_vol.cgns')

for n in range(3):
    cube.refine(['i', 'j'])

# combine grids
# cube = readGrid('cube_vol.cgns')
overset = readGrid('cube_xoverset.cgns')
final = combineGrids([cube, overset])
final.writeToCGNS('cube.cgns')




# extenc BC file for farfield
bc_file_str += """31 iLow bcfarfield far
31 iHigh bcfarfield far
31 kLow bcfarfield far
31 kHigh bcfarfield far
31 jLow bcinflow in
31 jHigh bcoutflowsubsonic out BCDataSet_1 BCOutFlowSubsonic Dirichlet Pressure 101300"""



# set BC
with open("bc_file", 'w') as f:
    f.write(bc_file_str)

grid = readGrid("cube.cgns")
grid.overwriteBCs('bc_file')
grid.writeToCGNS("cube.cgns")

