#!/bin/bash

manifold_dir=/home/wangjunlin/project/Manifold
project_dir=/home/wangjunlin/project/Contact-TransGrasp
log_path=/home/wangjunlin/project/log.txt
outlier_path=/home/wangjunlin/project/outlier.txt

# generate watertight versions and simplify them
echo "=> Generating and simplifying watertight versions of meshes..."
cd $manifold_dir/build
for file in $project_dir/data/meshes/objects/*.obj
do
    ./manifold $file $file -s >> $log_path
    ./simplify -i $file -o $file -m -r 0.02 >> $log_path
done

# find outliers
echo "=> Finding outliers..."
cd $project_dir/dataset
python3 find_outlier.py --log_path $log_path --outlier_save_path $outlier_path

# remove outliers
echo "=> Removing outliers..."
cd $project_dir/data/meshes/objects
while read line
do
    rm ./$line*.obj
done <  $outlier_path

cd $project_dir/data/grasps/objects
while read line
do
    rm ./*$line*.h5
done <  $outlier_path
