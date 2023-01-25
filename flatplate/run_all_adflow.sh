

for dir in 'clean' 'acharya' 'blanchard' 'rumsey_comp' ;
do
	cd $dir
	bash run_all_levels.sh
	cd ..
done
