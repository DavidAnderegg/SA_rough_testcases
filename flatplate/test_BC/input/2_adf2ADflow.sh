#!/bin/bash

rm flatplate_split_L4.cgns
cgns_utils removeBC flatplate_split_L4_adf.cgns flatplate_split_L4.cgns

cgns_utils overwriteBC flatplate_split_L4.cgns bcfile

cgns_utils connect flatplate_split_L4.cgns 1e-12
