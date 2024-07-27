#!/bin/bash

### Paths to modify
acronym_dir=$1         # /**/acronym2
manifold_dir=$2        # /**/Manifold
grasp_dir=$3           # The directory where grasp files (.h5) are stored. 
mesh_dir=$4            # The directory where mesh files (.obj) are stored. 
support_scale=$5       # A scaling ratio of the supporting object.
objects_per_scene=$6   # The number of objects per scene.
grasps_per_scene=$7    # The number of grasps per scene.
total_samples=$8       # The number of generated samples.
log_path=$acronym_dir/log.txt
outlier_path=$acronym_dir/outlier.txt

### Create directories for storing generated data.
mkdir -p data/grasps/objects
mkdir -p data/grasps/scenes
mkdir -p data/meshes/objects
mkdir -p data/meshes/scenes
object_grasp_dir=$acronym_dir/data/grasps/objects
object_mesh_dir=$acronym_dir/data/meshes/objects
scene_grasp_dir=$acronym_dir/data/grasps/scenes
scene_mesh_dir=$acronym_dir/data/meshes/scenes

### Sample objects (grasps + meshes)
echo "Sampling objects..."
cd $acronym_dir/scripts
python sample_mesh.py --object_dir $grasp_dir --mesh_dir $mesh_dir \
--object_save_dir $object_grasp_dir --mesh_save_dir $object_mesh_dir

### Generate watertight meshes and simplify the meshes
echo "Generating simplified watertight meshes..."
cd $manifold_dir/build
for file in $object_mesh_dir/*.obj
do
    ./manifold $file $file -s >> $log_path
    ./simplify -i $file -o $file -m -r 0.02 >> $log_path
done

# Search for meshes with outliers
echo "Searching for outliers..."
cd $acronym_dir/scripts
python find_outlier.py --log_path $log_path --outlier_save_path $outlier_path

echo "Handling outliers..."
cd $object_mesh_dir
while read line
do
    rm -f ./$line*.obj
done <  $outlier_path

cd $object_grasp_dir
while read line
do
    rm -f ./*$line*.h5
done <  $outlier_path

### Generate multi-object scenes
echo "Generating samples..."
cd $acronym_dir/scripts
python generate_scene.py --object_dir $object_grasp_dir \
--object_mesh_dir $object_mesh_dir --support_mesh_dir $acronym_dir/supports \
--grasp_save_dir $scene_grasp_dir --mesh_save_dir $scene_mesh_dir \
--support_scale $support_scale --num_object $objects_per_scene \
--num_grasp $grasps_per_scene --num_sample $total_samples

echo "Completed."
rm -f $log_path
rm -f $outlier_path
rm -f -r $object_grasp_dir
rm -f -r $object_mesh_dir
