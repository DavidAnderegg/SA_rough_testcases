

for i in {4..0..-1}
do
	for ks in '0' '1.0e-04' '1.0e-03';
	do
		mpirun -np 6 SU2_CFD flatplate_rumsey_comp_ks${ks}_L${i}.cfg
	done
done
