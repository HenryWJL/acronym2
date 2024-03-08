#!/bin/bash

### Need to modify
acronym_dir=/.../acronym_2.0
manifold_dir=/.../Manifold
mesh_dir=/...
###
log_path=$acronym_dir/log.txt
outlier_path=$acronym_dir/outlier.txt

# generate watertight versions and simplify
echo "Generating simplified watertight versions..."
cd $manifold_dir/build
for file in $mesh_dir/*.obj
do
    ./manifold $file $file -s >> $log_path
    ./simplify -i $file -o $file -m -r 0.02 >> $log_path
done

# search outliers
echo "Searching outliers..."
cd $acronym_dir
python find_outlier.py --log_path $log_path --outlier_save_path $outlier_path

# remove outliers
echo "Removing outliers..."
cd $mesh_dir
while read line
do
    rm ./$line*.obj
done <  $outlier_path

cd $project_dir/data/grasps/objects
while read line
do
    rm ./*$line*.h5
done <  $outlier_path

echo "Completed"
rm -f $log_path
rm -f $outlier_path
