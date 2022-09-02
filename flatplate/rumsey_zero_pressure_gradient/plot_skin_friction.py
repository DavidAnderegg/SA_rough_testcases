import matplotlib.pyplot as plt
import numpy as np
import os
import copy
import h5py


def extract_values(wall):
    """
    extracts the coordinates and skrinfriction + stanton number from a given wall
    """
    coords = list()

    for axis in ['X', 'Z']:
        coordinate = wall[f'GridCoordinates/Coordinate{axis}/ data']
        coord_mean = (coordinate[:,0] + coordinate[:,1]) / 2
        coords.append(coord_mean)

    cf = wall[f'Flow solution/SkinFrictionMagnitude/ data']
    ch = wall[f'Flow solution/StantonNumber/ data']

    cf = np.array(cf)[:,0]
    coords = np.array(coords).transpose()

    return coords, cf, ch

def extract_cf(wall):
    coords, cf, ch = extract_values(wall)

    cf_new = copy.deepcopy(coords)
    cf_new[:,1] = cf[:-1]

    return cf_new



def main():
    # finishes = ['clean', 'ks1.0e-04', 'ks1.5e-03']
    level = 'L0'

    # Comparsion Data
    cfl3d = np.loadtxt(os.path.join('data', 'CFL3D_cf.dat'))
    plt.plot(cfl3d[:,0], cfl3d[:,1], '-', label='CFL3D')

    fun3d = np.loadtxt(os.path.join('data', 'FUN3D_cf.dat'))
    plt.plot(fun3d[:,0], fun3d[:,1], '-', label='FUND3')


    # read data from cgns-surface file
    cgns_file = h5py.File(os.path.join('output', f'flatplate_rumsey_{level}_surf_hdf.cgns'), 'r')

    # find surfaces
    data = cgns_file['BaseSurfaceSol']

    surfaces = list()
    for key in data.keys():
        if 'NSWallAdiabaticBC' in key:
            surfaces.append(data[key])

    # extract and plot cf
    data = extract_cf(surfaces[0])
    plt.plot(data[:,0], data[:,1], label=f'ADflow')



    ax = plt.gca()
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0, 6e-3)
    ax.set_ylabel('$C_f$')
    ax.set_xlabel('x [m]')
    ax.grid()
    ax.legend()
    plt.suptitle(f'Flat plate, Zero pressure gradient, Rumsey, {level}')
    plt.show()

if __name__ == '__main__':
    main()
