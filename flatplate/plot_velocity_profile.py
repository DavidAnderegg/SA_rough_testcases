import matplotlib.pyplot as plt
import numpy as np
import os
import copy
import argparse
import h5py

from testcases import testcases, levels
from functions import load_solution, sort_legend



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
    for name, path in case['vp_comp_data'].items():
        data = np.loadtxt(os.path.join(case['base_path'], 'data', path))
        axs.plot(data[:,0], data[:,1], '+', label=name)

    for finish in case['finishes']:
        Solution = None
        for level in levels:
            # load solution files
            Solution = load_solution(case, finish, level)
            if Solution == False:
                continue


            for x in case['vp_x_positions']:
                # extract needed values from solutions
                u, y, rho, cf = Solution.velocity_profile(x)
                t_inf, p_inf, u_inf, mu_inf, rho_inf = Solution.initial_conditions()

                tau = 1/2 * cf * u[-1]**2
                u_star = np.sqrt(tau)


                y_plus = (y * rho_inf * u_star) / mu_inf
                u_plus = u / u_star

                # convert ks to ks+
                label = finish
                if 'ks' in finish:
                    ks_str = finish.split('ks')[1]
                    ks = float(ks_str)
                    # ks = 1.1e-3
                    # ks = 4.0e-4
                    ks_plus = ks * u_star / (mu_inf / rho_inf)

                    label = f'$ks^+$ {ks_plus:.0f}'


                axs.plot(y_plus, u_plus, label=f'ADflow x={x}, {level}, {label}')

            # break loop as we have the finest grid
            break

        if Solution is None:
            continue

        u_plus, y_plus = None, None
        if finish == 'clean':
            # plot theory
            # viscous sublayer
            y_plus = np.linspace(1e-3, 1.5e1, 100)
            u_plus = y_plus
            axs.plot(y_plus, u_plus, '--')

            #log law
            kappa, C_plus = 0.41, 5.0
            y_plus = np.linspace(5e0, 1e4, 100)
            u_plus = 1/kappa * np.log(y_plus) + C_plus
        elif 'ks' in finish:
            kappa = 0.41
            y_plus = np.linspace(5e0, 1e4, len(rho))
            y = (y_plus * mu_inf) / (rho * u_star)
            u_plus = 1/kappa * np.log(y/ks) + 8.5

        if u_plus is not None and y_plus is not None:
            axs.plot(y_plus, u_plus, '--', label=f'Theory {label}')






    plt.xscale('log')
    # ax.set_xlim(case['cf_limits']['x'])
    # ax.set_xlim(1, 1e4)
    # ax.set_ylim(case['cf_limits']['y'])
    axs.set_ylabel('$u+$')
    axs.set_xlabel('$y+$')
    axs.grid()
    sort_legend(axs)
    plt.suptitle(f'Flat plate, Zero pressure gradient, {args.case}')
    plt.show()

if __name__ == '__main__':
    main()
