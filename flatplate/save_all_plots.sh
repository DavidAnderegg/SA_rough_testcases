#!/bin/bash

cases=('clean' 'rumsey_comp' 'blanchard' 'acharya')

plots=('plot_grid_convergence.py' 'plot_skin_friction.py' 'plot_velocity_profile.py')



for case in "${cases[@]}"; do
    for plot in "${plots[@]}"; do
        python $plot -case $case -save 1
    done
done
