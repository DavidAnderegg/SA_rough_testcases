

for i in {4..0..-1}
do
	for ks in '0' '5e-04' '1.205e-03' '2.0e-3';
	do
		mpirun -np 6 python run_acharya.py -level $i -ks $ks
	done
done
