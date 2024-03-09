#!/bin/bash

acronym_dir=$1         # /.../acronym2
manifold_dir=$2        # /.../Manifold
grasp_dir=$3           # where you store downloaded grasp data (.h5 files)
mesh_dir=$4            # where you store downloaded mesh data (.obj files)
support_scale=$5       # a scaling ratio, depending on the supporting object itself
objects_per_scene=$6   # how many objects in a scene
grasps_per_scene=$7    # how many grasps preserved in a scene
total_samples=$8       # how many samples to generate
log_path=$acronym_dir/log.txt
outlier_path=$acronym_dir/outlier.txt

### prepare directories
mkdir -p data/grasps/objects
mkdir -p data/grasps/scenes
mkdir -p data/meshes/objects
mkdir -p data/meshes/scenes
object_grasp_dir=$acronym_dir/data/grasps/objects
object_mesh_dir=$acronym_dir/data/meshes/objects
scene_grasp_dir=$acronym_dir/data/grasps/scenes
scene_mesh_dir=$acronym_dir/data/meshes/scenes

### sample objects (grasps + meshes)
echo "Sampling objects..."
python sample_mesh.py --object_dir $grasp_dir --mesh_dir $mesh_dir \
--object_save_dir $object_grasp_dir --mesh_save_dir $object_mesh_dir

### generate watertight versions and simplify
echo "Generating simplified watertight versions..."
cd $manifold_dir/build
for file in $object_mesh_dir/*.obj
do
    ./manifold $file $file -s >> $log_path
    ./simplify -i $file -o $file -m -r 0.02 >> $log_path
done

# search outliers and handle
echo "Searching outliers..."
cd $acronym_dir
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

### generate multi-object scenes
cd $acronym_dir
python generate_scene.py --object_dir $object_grasp_dir \
--object_mesh_dir $object_mesh_dir --support_mesh_dir $acronym_dir/supports \
--grasp_save_dir $scene_grasp_dir --mesh_save_dir $scene_mesh_dir \
--support_scale $support_scale --num_object $objects_per_scene \
--num_grasp $grasps_per_scene --num_sample $total_samples

echo "Completed!"
rm -f $log_path
rm -f $outlier_path
rm -f -r $object_grasp_dir
rm -f -r $object_mesh_dir
