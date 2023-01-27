import numpy as np
from scipy.spatial.transform import Rotation as R
from pyhyp import pyHyp
from cgnsutilities.cgnsutilities import Grid, readGrid
from idwarp import USMesh


ks_rough = 1.0
ks_clean = 0.1


# extrude cube-mesh and prepare bc-file
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
    "outerFaceBC": "farfield",
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


# overwrite farfield with wall (this way it is possible to warp)
grid = readGrid("cube_vol.cgns")
grid.overwriteBCFamilyWithBC('Far', 'bcwall')
grid.writeToCGNS("cube_vol_pre.cgns")


#  rotate cube by 45° in all directions
options = {
    "gridfile": "cube_vol_pre.cgns",
    "LdefFact": 50.0,
    # "aExp": 4.0
    "alpha": 0.20,
}
mesh = USMesh(options=options)

# get all surface coordinates and filter only those where at least one axis == 0.5
coords_all = mesh.getSurfaceCoordinates().copy()
indx = np.argwhere(np.logical_or(
    np.abs(coords_all[:,0]) == 0.5,
    np.logical_or(
    np.abs(coords_all[:,1]) == 0.5,
    np.abs(coords_all[:,2]) == 0.5
    )
)).flatten()
coords = coords_all[indx]

# create rotation matrix and rotate surface coords
a = 0
r = R.from_euler('zyx', [a, a, a], degrees=True)
# r = R.from_euler('x', [30], degrees=True)
# r = R.from_euler('x', [0], degrees=True)
coords_rot = r.apply(coords)


# warp and save mesh
coords_all[indx] = coords_rot
mesh.setSurfaceCoordinates(coords_all)
mesh.warpMesh()
mesh.writeGrid("cube_vol_post.cgns")


# set Farfield and roughness values
with open("bc_file", 'w') as f:
    f.write(bc_file_str)

grid = readGrid("cube_vol_post.cgns")
grid.overwriteBCFamilyWithBC('Far', 'bcfarfield')
grid.overwriteBCs('bc_file')
grid.writeToCGNS("cube.cgns")

# set roughness value


