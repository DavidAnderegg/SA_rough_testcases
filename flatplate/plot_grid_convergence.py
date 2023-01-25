import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

from testcases import testcases
from functions import ADF_load_solution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-case', type=str, default='rumsey',
                    help='The Test-case to plot, possible values are: rumsey, blanchard, acharya')
    args = parser.parse_args()

    case = testcases[args.case]

    N = np.array([208896, 52224, 13056, 3264, 816])
    h = 1/N**(1/2)

    s = 2
    fig = plt.figure(figsize=(6.4*s, 4.8*s), layout='tight')
    axs = fig.subplots(2, 2)
    axs = axs.flatten()

    xp = np.ones_like(h) * np.nan
    xv = np.ones_like(N) * np.nan
    xm = np.ones_like(N) * np.nan
    cd = np.ones_like(N) * np.nan

    for finish in case['finishes']:
        for n in range(len(case['levels'])):
            level = case['levels'][n]
            Solution = ADF_load_solution(case, finish, level)
            if Solution == False:
                continue
            raw_polar = Solution.polar()


            xp[n] = raw_polar['forcexpressure']
            xv[n] = raw_polar['forcexviscous']
            xm[n] = -raw_polar['forcexmomentum']
            cd[n] = raw_polar['cd']

        axs[0].plot(h, xp, '*-', label=finish)
        axs[1].plot(h, xv, '*-')
        axs[2].plot(h, xm, '*-')
        axs[3].plot(h, cd, '*-')

    for ax in axs:
        ax.set_xlabel('$\\sqrt{\\frac{1}{N}}$')
        ax.grid()
    axs[0].set_ylabel('$force_{pressure}$')
    axs[1].set_ylabel('$force_{viscous}$')
    axs[2].set_ylabel('$force_{momentum}$')
    axs[3].set_ylabel('$C_d$')
    axs[0].legend()
    plt.suptitle(f'Flat plate, Zero pressure gradient, {args.case}')
    plt.show()




if __name__ == '__main__':
    main()
