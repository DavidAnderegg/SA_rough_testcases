import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import argparse

plt.style.use('tableau-colorblind10')

from testcases import testcases
from functions import ADF_load_solution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-case', type=str, default='rumsey',
                    help='The Test-case to plot, possible values are: rumsey, blanchard, acharya')
    parser.add_argument('-save', type=int, default=0,
                        help='Saves the plot when set to 1')
    args = parser.parse_args()

    # set style stuff
    mpl.rcParams['font.family'] = 'Avenir'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.linewidth'] = 2

    case = testcases[args.case]

    N = np.array([208896, 52224, 13056, 3264, 816])
    h = 1/N**(1/2)

    s = 1.5
    fig = plt.figure(figsize=(6.4*s, 4.8*s), layout='tight')
    axs = fig.subplots(2, 2)
    axs = axs.flatten()

    # Edit the major and minor ticks of the x and y axes
    for ax in axs:
        ax.xaxis.set_tick_params(which='major', size=10, width=1.5, direction='in')
        ax.yaxis.set_tick_params(which='major', size=10, width=1.5, direction='in')
        ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in')
        ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in')


    xp = np.ones_like(h) * np.nan
    xv = np.ones_like(N) * np.nan
    xm = np.ones_like(N) * np.nan
    cd = np.ones_like(N) * np.nan
    cf = np.ones_like(N) * np.nan

    # cf_x = 1.0
    cf_x = case['vp_x_positions'][0]

    for finish in case['finishes']:
        for n in range(len(case['levels'])):
            level = case['levels'][n]
            Solution = ADF_load_solution(case, finish, level)
            if Solution == False:
                continue
            raw_polar = Solution.polar()


            _, _, _, _, local_cf = Solution.velocity_profile(cf_x)

            xp[n] = raw_polar['forcexpressure']
            xv[n] = raw_polar['forcexviscous']
            xm[n] = -raw_polar['forcexmomentum']
            cd[n] = raw_polar['cd']
            cf[n] = local_cf

        # axs[0].plot(h, xp, '*-', label=finish)
        axs[0].plot(h, cf, '*-', label=finish)
        axs[1].plot(h, xv, '*-')
        axs[2].plot(h, xm, '*-')
        axs[3].plot(h, cd, '*-')

    for ax in axs:
        ax.set_xlabel('$\\sqrt{\\frac{1}{N}}$', labelpad=5)
        ax.set_xlim(0, None)
    # axs[0].set_ylabel('$force_{pressure}$', labelpad=5)
    axs[0].set_ylabel(f'$C_f$ @ x={cf_x}', labelpad=5)
    axs[1].set_ylabel('$force_{viscous}$', labelpad=5)
    axs[2].set_ylabel('$force_{momentum}$', labelpad=5)
    axs[3].set_ylabel('$C_d$', labelpad=5)
    axs[0].legend(frameon=False, fontsize=10, borderpad=1)

    if not args.save:
        plt.suptitle(f'Flat plate, Zero pressure gradient, {args.case}')
        plt.show()
    else:
        d = 'plots'
        if not os.path.exists(d):
            os.makedirs(d)

        plt.savefig(
            os.path.join(d, f'gc_{args.case}.pdf'),
            dpi=300, transparent=False, bbox_inches='tight'
        )



if __name__ == '__main__':
    main()
