
testcases = {
    'clean': {
        'levels': ['L0', 'L1', 'L2', 'L3', 'L4'],
        'base_path': 'clean',
        'ADF_polar_file': 'flatplate_{finish}_{level}.out',
        'ADF_surface_file': 'flatplate_{finish}_{level}_surf_hdf.cgns',
        'ADF_volume_file': 'flatplate_{finish}_{level}_vol_hdf.cgns',
        'finishes': ['clean'],
        'cf_comp_data': {
            'CFL3D, $k_s^+ = 0$': 'CFL3D_cf.dat',
            # 'FUN3D': 'FUN3D_cf.dat',
        },
        'cf_limits': {
            'x': [-0.08, 2],
            'y': [0.002, 0.006],
        },
        'vp_comp_data': {
            'CFL3D, $x=0.97$, $k_s^+ = 0$': 'u+y+_x0.97008.dat',
            'CFL3D, $x=1.9$, $k_s^+ = 0$': 'u+y+_x1.90334.dat',
        },
        'vp_x_positions': [0.97, 1.97],
    },
    'blanchard': {
        'levels': ['L0', 'L1', 'L2', 'L3', 'L4'],
        'base_path': 'blanchard',
        'ADF_polar_file': 'flatplate_blanchard_{finish}_{level}.out',
        'ADF_surface_file': 'flatplate_blanchard_{finish}_{level}_surf_hdf.cgns',
        'ADF_volume_file': 'flatplate_blanchard_{finish}_{level}_vol_hdf.cgns',
        'finishes': ['clean', 'ks1.095e-03', 'ks1.3e-03'],
        'cf_comp_data': {
            'Experiment, $k_s^+ \\approx 150$': '0pressGrad_cf_exp.csv',
        },
        'cf_limits': {
            'x': [-0.017, 0.5],
            'y': [0.002, 0.014],
        },
        'vp_comp_data': {},
        'vp_x_positions': [0.5],
    },
    'acharya': {
        'levels': ['L0', 'L1', 'L2', 'L3', 'L4'],
        'base_path': 'acharya',
        'ADF_polar_file': 'flatplate_ancharya_{finish}_{level}.out',
        'ADF_surface_file': 'flatplate_ancharya_{finish}_{level}_surf_hdf.cgns',
        'ADF_volume_file': 'flatplate_ancharya_{finish}_{level}_vol_hdf.cgns',
        'finishes': ['clean', 'ks5.000e-04', 'ks1.205e-03', 'ks2.000e-03'], #, 'ks4.0e-04', 'ks1.1e-03'],
        'finishes': ['clean', 'ks5.000e-04', 'ks1.205e-03'], #, 'ks4.0e-04', 'ks1.1e-03'],
        'cf_comp_data': {
            'SRS1, $k_s^+ \\approx 25$': 'cf_SRS1.dat',
            'SRS2, $k_s^+ \\approx 70$': 'cf_SRS2.dat',
        },
        'cf_limits': {
            'x': [-0.10, 3],
            'y': [0.002, 0.01],
        },
        'vp_comp_data': {
            'Mean SRS2 $ks^+$ ~70': 'vp_SRS2.dat',
        },
        'vp_x_positions': [1.97],
    },
    'rumsey_comp': {
        'levels': ['L0', 'L1', 'L2', 'L3', 'L4'],
        'base_path': 'rumsey_comp',
        'ADF_polar_file': 'flatplate_rumsey_comp_{finish}_{level}.out',
        'ADF_surface_file': 'flatplate_rumsey_comp_{finish}_{level}_surf_hdf.cgns',
        'ADF_volume_file': 'flatplate_rumsey_comp_{finish}_{level}_vol_hdf.cgns',
        'SU2_surface_file': 'surface_flow_{finish}_{level}.vtu',
        'SU2_volume_file': 'flow_{finish}_{level}.vtu',
        'finishes': ['clean', 'ks1.0e-04', 'ks1.0e-03'],
        'cf_comp_data': {},
        'cf_limits': {
            'x': [-0.08, 2],
            'y': [0.002, 0.01],
        },
        'vp_comp_data': {},
        'vp_x_positions': [1.5],
    },
    'test_BC': {
        'levels': ['L4'],
        'base_path': 'test_BC',
        'ADF_polar_file': 'flatplate_test_BC_{finish}_{level}.out',
        'ADF_surface_file': 'flatplate_test_BC_{finish}_{level}_surf_hdf.cgns',
        'ADF_volume_file': 'flatplate_test_BC_{finish}_{level}_vol_hdf.cgns',
        'finishes': ['clean', 'last1_ks1.0e-03', 'last10_ks1.0e-03'],
        'cf_comp_data': {},
        'cf_limits': {
            'x': [0, 2],
            'y': [0, 0.008],
        },
        'vp_comp_data': {},
        'vp_x_positions': [1.5],
    },

}
