#!/bin/bash

rm flatplate_L$1.cgns
cgns_utils removeBC flatplate_L$1_adf.cgns flatplate_L$1.cgns

if [[ $1 -eq 0 ]]; then
    cgns_utils overwriteBC flatplate_L$1.cgns bcfile_L0
else
    cgns_utils overwriteBC flatplate_L$1.cgns bcfile
fi

cgns_utils connect flatplate_L$1.cgns 1e-12
