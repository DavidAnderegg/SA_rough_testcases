import numpy as np
import os
import copy
import h5py
import operator
import vtk
from vtk.util.numpy_support import vtk_to_numpy as vtk2np

def sort_legend(axs):
    handles, labels = axs.get_legend_handles_labels()
    hl = sorted(zip(handles, labels),
            key=operator.itemgetter(1))
    handles2, labels2 = zip(*hl)
    axs.legend(handles2, labels2)


def ADF_load_solution(case, finish, level):
    cgns_vol_file = os.path.join(
        case['base_path'], 'output',
        case['ADF_volume_file'].format(finish=finish, level=level)
    )
    if not os.path.exists(cgns_vol_file):
        return False

    cgns_surf_file = os.path.join(
        case['base_path'], 'output',
        case['ADF_surface_file'].format(finish=finish, level=level)
    )
    if not os.path.exists(cgns_surf_file):
        return False

    polar_file = os.path.join(
        case['base_path'],
        case['ADF_polar_file'].format(finish=finish, level=level)
    )
    if not os.path.exists(polar_file):
        return False

    Solution = ADF_FlatPlateSolution(cgns_vol_file, cgns_surf_file, polar_file)

    return Solution

def SU2_load_solution(case, finish, level):
    try:
        vtu_vol_file = os.path.join(
            case['base_path'], 'SU2',
            case['SU2_volume_file'].format(finish=finish, level=level)
        )
        if not os.path.exists(vtu_vol_file):
            return False
    except:
        return False

    try:
        vtu_surf_file = os.path.join(
            case['base_path'], 'SU2',
            case['SU2_surface_file'].format(finish=finish, level=level)
        )
        if not os.path.exists(vtu_surf_file):
            return False
    except:
        return False

    Solution = SU2_FlatPlateSolution(vtu_vol_file, vtu_surf_file)

    return Solution


class ADF_FlatPlateSolution:
    def __init__(self, volume_file, surface_file, polar_file):
        self.vol_data = self._read_cgns_file(volume_file)
        self.surf_data = self._read_cgns_file(surface_file)
        self.polar_data = self._read_polar_file(polar_file)


    def initial_conditions(self):
        t_inf, p_inf, u_inf= -1, -1, -1

        state = 0
        for line in self.polar_data:

            if 'Aero Options' in line:
                state = 1
                continue

            if state == 1:
                if 'RESULTS' in line:
                    break

                if 'T' in line:
                    t_inf = float(line.split()[1])
                if 'P' in line:
                    p_inf = float(line.split()[1])
                if 'V' in line:
                    u_inf = float(line.split()[1])


        C, T0, mu0 = 120, 291.15, 18.27e-6
        mu_inf = mu0 * ((T0 + C) / (t_inf + C)) * ((t_inf/T0)**(3/2))

        rho_inf = p_inf / (t_inf * 287)

        return t_inf, p_inf, u_inf, mu_inf, rho_inf

    def ref_state(self):
        p_ref = self.vol_data['BASE#1']['ReferenceState']['Pressure'][' data'][0]
        t_ref = self.vol_data['BASE#1']['ReferenceState']['Temperature'][' data'][0]
        rho_ref = self.vol_data['BASE#1']['ReferenceState']['Density'][' data'][0]
        mu_ref = np.sqrt(p_ref * rho_ref)
        mach = self.vol_data['BASE#1']['ReferenceState']['Mach'][' data'][0]

        return p_ref, t_ref, rho_ref, mu_ref, mach


    def velocity_profile(self, x=1.0, eps=0.05):
        # get rev values so velocity can be non-dimensionalized
        p_ref, t_ref, rho_ref, mu_ref, mach = self.ref_state()
        t_inf, p_inf, u_inf, mu_inf, rho_inf = self.initial_conditions()

        # iterate through all Zones
        z_coords, x_velocity = None, None
        for zone_name, zone_data in self.vol_data['BASE#1'].items():
            # Find zones and skip rest
            try:
                if not 'ZoneType' in zone_data:
                    continue
            except AttributeError:
                continue

            # get x-coordinates + cf and figure out which one to use
            _, cf = self.local_cf()
            x_coords = zone_data['GridCoordinates']['CoordinateX'][' data'][0,:][:,0]

            diff = np.absolute(x_coords - x)
            index = diff.argmin()

            # lets skip  this zone if the error is bigger than 'eps'
            if np.abs(x_coords[index] - x) > eps:
                continue

            # extract z-values
            z_coords = zone_data['GridCoordinates']['CoordinateZ'][' data'][:,index][:,1]

            # extract velocity
            x_velocity = zone_data['Flow solution']['VelocityX'][' data'][:,index][:,1]
            p = zone_data['Flow solution']['Pressure'][' data'][:,index][:,1]
            rho = zone_data['Flow solution']['Density'][' data'][:,index][:,1]
            u = mach * np.sqrt(1.4*p/rho)

            # dimensionalize velocity
            x_velocity = x_velocity / u * u_inf

            # velocity is given on nodes, coords on centers -> 1 value to much for velocity
            x_velocity = x_velocity[:-1] + np.diff(x_velocity)

            # extract density
            rho = zone_data['Flow solution']['Density'][' data'][:,index][:,1]
            rho = rho * rho_ref
            rho = rho[:-1] + np.diff(rho)

            # return values
            return  x_velocity, z_coords, rho, np.array([mu_inf]), cf[index]

        return np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

    def local_cf(self):
        data = self.surf_data['BaseSurfaceSol']

        surface = None
        x_coords = np.array([])
        cf = np.array([])
        for key in data.keys():
            if not 'NSWallAdiabaticBC' in key:
                # surface= data[key]
                # break
                continue

            surface= data[key]

            x_coords = np.append(x_coords, surface['GridCoordinates']['CoordinateX'][' data'][:,0])
            cf_tmp = surface['Flow solution']['SkinFrictionMagnitude'][' data'][:,0]
            # cf is given on nodes, coords on centers -> 1 value to much for velocity
            cf_tmp = cf_tmp[:-1] + np.diff(cf_tmp)
            cf = np.append(cf, cf_tmp)

        return x_coords, cf

    def total_cf(self):
        x_coords, cf = self.local_cf()
        total_cf = np.trapz(cf, x_coords) / (x_coords[-1] - x_coords[0])

        # total_cf = np.average(cf)

        return total_cf

    def polar(self):
        header_str, n = '', 0
        lines = copy.copy(self.polar_data)
        for n in range(len(lines)):
            if 'RESULTS' in lines[n]:
                header_str = lines[n+1]
                break

        # read the 'header'-line
        header = header_str.split()

        # read the polars to dict
        polar_raw = np.array(lines[n + 3].split(), dtype=float)

        # save it in a nice dict
        polars = dict()
        for n in range(len(header)):
            polars[header[n]] = polar_raw[n]

        return polars



    @staticmethod
    def _read_cgns_file(file_path):
        return h5py.File(file_path, 'r')

    @staticmethod
    def _read_polar_file(polar_file):
        f = open(polar_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

class SU2_FlatPlateSolution:
    def __init__(self, volume_file, surface_file):
        self.vol_data = self._read_vtu_file(volume_file)
        self.surf_data = self._read_vtu_file(surface_file)

    def velocity_profile(self, x=1.0, eps=0.01):

        # first, lets find the x-coords to use
        x_coords, cf = self.local_cf()
        diff = np.absolute(x_coords - x)
        index = diff.argmin()

        # lets skip  this zone if the error is bigger than 'eps'
        if np.abs(x_coords[index] - x) > eps:
            return np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

        x_value = x_coords[index]
        cf_value = cf[index]

        # now, we can find all the indexes of the volume file that have this x-axis
        coords = vtk2np(self.vol_data.GetPoints().GetData())
        ind = np.argwhere(coords[:,0] == x_value).T.flatten()

        # lets find the z-coords
        z_coords = coords[ind]
        z_coords = z_coords[2:]
        z_coords = 2 - z_coords[:,1]*(-1)

        # lets find the x-velocity
        momentum = vtk2np(self.vol_data.GetPointData().GetArray("Momentum"))
        momentum = momentum[ind]
        momentum = momentum[2:]
        momentum = momentum[:,0]

        rho = vtk2np(self.vol_data.GetPointData().GetArray("Density"))
        rho = rho[ind]
        rho = rho[2:]

        mu = vtk2np(self.vol_data.GetPointData().GetArray("Laminar_Viscosity"))
        mu = mu[ind]
        mu = mu[2:]

        x_velocity = momentum / rho

        return x_velocity, z_coords, rho, mu, cf_value

    def local_cf(self):
        # first, lets find the x-coords
        coords = vtk2np(self.surf_data.GetPoints().GetData())
        x_coords = coords[:,0]

        # now, lets find cf
        cf = vtk2np(self.surf_data.GetPointData().GetArray("Skin_Friction_Coefficient"))
        cf = cf[:,0]

        return x_coords[1:], cf[1:]





    @ staticmethod
    def _read_vtu_file(file_path):
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_path)
        reader.Update()
        output = reader.GetOutput()

        return output
