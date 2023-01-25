

for i in {4..0..-1}
do
	for ks in '0' '1.095e-03' ;
	do
		mpirun -np 6 python run_blanchard.py -level $i -ks $ks
	done
done
