#!/bin/bash

# Converts the output-surface files from 'adf' to 'hdf5'

folders=('blanchard_zero_pressure_gradient' 'rumsey_zero_pressure_gradient' 'acharya_zero_pressure_gradient' 'rumsey_comp', 'test_BC')


for folder in "${folders[@]}"; do
    for file in ${folder}/output/*_surf.cgns; do
	filename=$(basename -- "$file")
	cgnsconvert -h -f $file ${folder}/output/${filename%.*}_hdf.cgns
    done
    for file in ${folder}/output/*_vol.cgns; do
	filename=$(basename -- "$file")
	cgnsconvert -h -f $file ${folder}/output/${filename%.*}_hdf.cgns
    done

done
