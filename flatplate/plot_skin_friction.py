import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

from testcases import testcases
from functions import ADF_load_solution, SU2_load_solution, sort_legend



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-case', type=str, default='rumsey',
                    help='The Test-case to plot, possible values are: rumsey, blanchard, acharya')
    args = parser.parse_args()
    case = testcases[args.case]

    s = 2
    fig = plt.figure(figsize=(6.4*s, 4.8*s), layout='tight')
    axs = fig.subplots(1,1)


    # Comparsion Data
    for name, path in case['cf_comp_data'].items():
        data = np.loadtxt(os.path.join(case['base_path'], 'data', path))
        axs.plot(data[:,0], data[:,1], '+', label=name)


    finish =''
    for finish in case['finishes']:
        label, mu_inf, u_inf, ks = '', 0, 0, 0
        ADF_Solution = None
        for level in case['levels']:
            # read data from cgns-surface file
            ADF_Solution = ADF_load_solution(case, finish, level)
            if ADF_Solution == False:
                continue

            # convert ks to ks+
            t_inf, p_inf, u_inf, mu_inf, rho_inf = ADF_Solution.initial_conditions()
            u, y, rho, mu, cf = ADF_Solution.velocity_profile(1.97)

            tau = 1/2 * cf * u[-1]**2
            u_star = np.sqrt(tau)
            label = finish
            if 'ks' in finish:
                ks_str = finish.split('ks')[1]
                ks = float(ks_str)
                ks_plus = ks * u_star / (mu_inf / rho_inf)

                label = f'$ks^+$ {ks_plus:.0f}'

            # extract and plot cf
            x_coords, cf = ADF_Solution.local_cf()
            axs.plot(x_coords, cf, label=f'ADflow {level}, {label}')

            # break loop as we have the finest grid
            break

        if ADF_Solution is None:
            continue

        x = np.linspace(1e-6, case['cf_limits']['x'][1], num=300)
        cf = None
        # clean regime (schlichting page 644)
        if finish == 'clean':
            Re_x = u_inf * x / mu_inf
            cf = 0.02296 * Re_x**(-0.139)

        # rough regime (jaffer_rough page 6)
        # if 'ks' in finish:
        #     cf = (3.476 + 0.707 * np.log(x/ks))**(-2.46)

        if cf is not None:
            axs.plot(x, cf, '--', label=f'Theory {label}')

        SU2_Solution = None
        for level in case['levels']:
            SU2_Solution = SU2_load_solution(case, finish, level)
            if SU2_Solution == False:
                continue

            x_coords, cf = SU2_Solution.local_cf()
            axs.plot(x_coords, cf, label=f'SU2 {level}, {label}')





    axs.set_xlim(case['cf_limits']['x'])
    axs.set_ylim(case['cf_limits']['y'])
    axs.set_ylabel('$C_f$')
    axs.set_xlabel('x [m]')

    sort_legend(axs)

    axs.grid()
    plt.suptitle(f'Flat plate, Zero pressure gradient, {args.case}')
    plt.show()

if __name__ == '__main__':
    main()
