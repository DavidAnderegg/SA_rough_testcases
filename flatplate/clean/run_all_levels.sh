

for i in {4..0..-1}
do
	mpirun -np 6 python run_clean.py -level $i
done
