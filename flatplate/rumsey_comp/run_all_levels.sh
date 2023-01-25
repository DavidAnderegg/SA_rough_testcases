

for i in {4..0..-1}
do
	for ks in '0' '1.0e-04' '1.0e-03';
	do
		mpirun -np 6 python run_flatplate_rumsey_comp.py -level $i -ks $ks
	done
done
