import os
import shutil
import numpy as np
from scipy.spatial.transform import Rotation as R
from pyhyp import pyHyp
from cgnsutilities.cgnsutilities import Grid, readGrid
from idwarp import USMesh


ks_rough = 1.0
ks_clean = 0.1

if not os.path.exists('meshes'):
   os.makedirs('meshes')


def main():

    # delete old meshes folder
    # shutil.rmtree('meshes')

    # create new meshes folder
    # os.mkdir('meshes')

    # extrude the mesh
    families = {}
    for i in range(1, 7):
        families[i] = 'rough'
    for i in range(7, 25):
        families[i] = 'clean'

    options = {
        # ---------------------------
        #        Input Parameters
        # ---------------------------
        "fileType": 'CGNS',
        "inputFile": 'cuboid_surf.cgns',
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

    # extrude the basic mesh
    hyp = pyHyp(options=options)
    hyp.run()
    hyp.writeCGNS(os.path.join('meshes', "cuboid.cgns"))


    # kLow
    wall_face = 'kLow'
    grid = readGrid(os.path.join('meshes', "cuboid.cgns"))
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))

    # kHigh 
    wall_face = 'kHigh'
    flip_axis(grid, 'k')
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))


    # iLow
    wall_face = 'iLow'
    grid = readGrid(os.path.join('meshes', "cuboid.cgns"))
    swap_axis(grid, 'k_i')
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))

    # iHigh
    wall_face = 'iHigh'
    flip_axis(grid, 'i')
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))


    # jLow
    wall_face = 'jLow'
    grid = readGrid(os.path.join('meshes', "cuboid.cgns"))
    swap_axis(grid, 'j_k')
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))

    # jHigh
    wall_face = 'jHigh'
    flip_axis(grid, 'j')
    set_bcs(grid, families, wall_face)
    grid.writeToCGNS(os.path.join('meshes', f"cuboid_{wall_face}.cgns"))



def set_bcs(grid, families, wall_face='kLow'):

    # extrude cube-mesh and prepare bc-file
    wall_str = '{i} {wall_face} bcwall {family} BCDataSet_1 BCWall Dirichlet SandGrainRoughness {ks}\n'
    bc_file_str = ''
    for i in range(1, 7):
        bc_file_str += wall_str.format(i=i, wall_face=wall_face, family=families[i], ks=ks_rough)

    for i in range(7, 25):
        bc_file_str += wall_str.format(i=i, wall_face=wall_face, family=families[i],  ks=ks_clean)

    bc_file = os.path.join('meshes', 'bc_file')

    # save the file
    with open(bc_file, 'w') as f:
        f.write(bc_file_str)

    # clear all existing bc's and connectivity
    for blk in grid.blocks:
        blk.bocos = []
        blk.B2Bs = []
    grid.connect()

    # set roughness value
    grid.overwriteBCs(bc_file)

    # set farfield
    grid.fillOpenBCs(7, 'Far')

    # delete bc-file
    os.remove(bc_file)


def swap_axis(grid, axis):
    for blk in grid.blocks:
        blk.bocos = []
        blk.B2Bs = []

        if axis == 'i_j':
            newCoords = np.zeros((blk.dims[1], blk.dims[0], blk.dims[2], 3))
            for k in range(blk.dims[2]):
                for i in range(blk.dims[0]):
                    for idim in range(3):
                        newCoords[:, i, k, idim] = blk.coords[i, :, k, idim].copy()
                for j in range(blk.dims[1]):
                    for idim in range(3):
                        newCoords[j, :, k, idim] = blk.coords[:, j, k, idim].copy()

        elif axis == 'j_k':
            newCoords = np.zeros((blk.dims[0], blk.dims[2], blk.dims[1], 3))
            for i in range(blk.dims[0]):
                for j in range(blk.dims[1]):
                    for idim in range(3):
                        newCoords[i, :, j, idim] = blk.coords[i, j, :, idim].copy()
                for k in range(blk.dims[2]):
                    for idim in range(3):
                        newCoords[i, k, :, idim] = blk.coords[i, :, k, idim].copy()

        elif axis == 'k_i':
            newCoords = np.zeros((blk.dims[2], blk.dims[1], blk.dims[0], 3))
            for j in range(blk.dims[1]):
                for k in range(blk.dims[2]):
                    for idim in range(3):
                        newCoords[k, j, :, idim] = blk.coords[:, j, k, idim].copy()
                for i in range(blk.dims[0]):
                    for idim in range(3):
                        newCoords[:, j, i, idim] = blk.coords[i, j, :, idim].copy()


        blk.dims = list(newCoords.shape[0:3])
        blk.coords = newCoords.copy()

    # Finally reconnect
    grid.connect()


def flip_axis(grid, axis):
    for blk in grid.blocks:
        blk.bocos = []
        blk.B2Bs = []

        if axis == 'i':
            for k in range(blk.dims[2]):
                for j in range(blk.dims[1]):
                    for idim in range(3):
                        blk.coords[:, j, k, idim] = blk.coords[::-1, j, k, idim]
        elif axis == 'j':
            for k in range(blk.dims[2]):
                for i in range(blk.dims[0]):
                    for idim in range(3):
                        blk.coords[i, :, k, idim] = blk.coords[i, ::-1, k, idim]
        elif axis == 'k':
            for j in range(blk.dims[1]):
                for i in range(blk.dims[0]):
                    for idim in range(3):
                        blk.coords[i, j, :, idim] = blk.coords[i, j, ::-1, idim]

    # Finally reconnect
    grid.connect()



if __name__ == '__main__':
    main()
