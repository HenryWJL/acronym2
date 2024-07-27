"""
This is modified from https://github.com/NVlabs/acronym/blob/main/scripts/acronym_generate_scene.py
"""

import os
import sys
import random
import trimesh
import argparse
import h5py
import numpy as np
import trimesh.path
from glob import glob

from .utils import Scene, load_mesh, load_grasps


def make_parser():
    parser = argparse.ArgumentParser(
        description="Generate multi-objects scenes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--object_dir",
        default="",
        help="The directory used for loading graspable objects and their grasps."
    )
    parser.add_argument(
        "--object_mesh_dir",
        default="",
        help="The directory used for loading graspable objects' meshes."
    )
    parser.add_argument(
        "--support_mesh_dir",
        default="",
        help="The directory used for loading supporting objects' meshes."
    )
    parser.add_argument(
        "--gripper_path",
        default="../configs/franka_gripper_collision_mesh.stl",
        help="The gripper mesh used for collision check."
    )
    parser.add_argument(
        "--grasp_save_dir",
        default="",
        help="The directory used for saving scene grasps."
    )
    parser.add_argument(
        "--mesh_save_dir",
        default="",
        help="The directory used for saving scene meshes."
    )
    parser.add_argument(
        "--support_scale",
        default=0.020,
        help="The scaling factor of supporting objects' meshes."
    )
    parser.add_argument(
        "--num_object",
        default=10,
        help="The number of graspable objects per scene."
    )
    parser.add_argument(
        "--num_grasp",
        default=1000,
        help="The number of grasps per scene.",
    )
    parser.add_argument(
        "--num_sample",
        default=10000,
        help="The number of generated samples.",
    )
    return parser


def random_sample(array, n):
    '''
    Randomly sample n rows from the input array
    '''
    array_idx = np.arange(array.shape[0])
    np.random.shuffle(array_idx)
    array_sample = array[array_idx[0: n]]
    return array_sample
    

def main(argv=sys.argv[1:]):
    parser = make_parser()
    args = parser.parse_args(argv)
    
    # load graspable objects and supporting objects
    objects = glob(os.path.join(args.object_dir, "**.h5"))
    supports = glob(os.path.join(args.support_mesh_dir, "**.obj"))
    assert len(objects) != 0, "No graspable object available!"
    assert len(supports) != 0, "No supporting object available!"
    assert args.num_object <= len(objects), "Too many objects per scene!"
    
    for sample_idx in range(1, args.num_sample + 1):
        # randomly sample graspable objects and supporting objects
        objects_sample = random.sample(objects, args.num_object)
        supports_sample = random.sample(supports, 1)[0]
        # load graspable objects' meshes and supporting objects' meshes
        object_meshes = [load_mesh(o, mesh_root_dir=args.object_mesh_dir) for o in objects_sample]
        support_meshes = trimesh.load(supports_sample).apply_scale(args.support_scale)
        # generate scenes
        scene = Scene.random_arrangement(object_meshes, support_meshes)
        # load gripper mesh for collision check
        gripper_mesh = trimesh.load(args.gripper_path, 'stl')
        # get positive grasps and negative grasps
        T_positive = []  # positive grasps (success == 1 and collision free)
        T_negative = []  # negative grasps (success == 0 + success == 1 but collision)
        for idx, fname in enumerate(objects_sample):
            T, success = load_grasps(fname)
            obj_pose = scene._poses["obj{}".format(idx)]
            # check collisions
            collision_free = np.array(
                [
                    idx
                    for idx, t in enumerate(T[success == 1])
                    if not scene.in_collision_with(
                        gripper_mesh, transform=np.dot(obj_pose, t)
                    )
                ]
            )
            collision = np.array(
                [
                    idx
                    for idx, t in enumerate(T[success == 1])
                    if scene.in_collision_with(
                        gripper_mesh, transform=np.dot(obj_pose, t)
                    )
                ]
            )
            if len(collision_free) != 0:
                T_positive.append(
                    np.array(
                        [
                            np.dot(obj_pose, t)
                            for t in T[success == 1][collision_free]
                        ]
                    )
                )
            
            if len(collision) != 0:
                T_negative.append(
                    np.array(
                        [
                            np.dot(obj_pose, t)
                            for t in T[success == 0]
                        ]
                    )  
                ) 
                T_negative.append(
                    np.array(
                        [
                            np.dot(obj_pose, t)
                            for t in T[success == 1][collision]
                        ]
                    )  
                ) 
                    
            else:
                T_negative.append(
                    np.array(
                        [
                            np.dot(obj_pose, t)
                            for t in T[success == 0]
                        ]
                    )  
                ) 

        T_positive = np.concatenate([t for t in T_positive], axis=0)
        T_negative = np.concatenate([t for t in T_negative], axis=0)     
        # sample positive grasps and negative grasps
        T = None
        success = None
        if T_positive.shape[0] < args.num_grasp // 2:
            # too few positive grasps, may cause unbalance problems
            T_negative = random_sample(T_negative, args.num_grasp - T_positive.shape[0])
            T = np.concatenate([T_positive, T_negative], axis=0)
            success = np.concatenate([np.ones(T_positive.shape[0]), np.zeros(T_negative.shape[0])], axis=0)
            
        else:
            # approximately 1:1 sampling
            T_positive = random_sample(T_positive, args.num_grasp // 2)
            T_negative = random_sample(T_negative, args.num_grasp - args.num_grasp // 2)
            T = np.concatenate([T_positive, T_negative], axis=0)
            success = np.concatenate([np.ones(T_positive.shape[0]), np.zeros(T_negative.shape[0])], axis=0)
            
        # save grasps and scene meshes   
        grasp_save_path = os.path.join(args.grasp_save_dir, "%d.h5" % (sample_idx)) 
        scene_save_path = os.path.join(args.mesh_save_dir, "%d.obj" % (sample_idx))
        writer = h5py.File(grasp_save_path, 'a')
        writer.create_dataset("grasps/transforms", data=T)
        writer.create_dataset("grasps/qualities/flex/object_in_gripper", data=success)
        writer.create_dataset("object/file", data="%d.obj" % (sample_idx))
        writer.create_dataset("object/scale", data=1.0)
        scene = scene.colorize().as_trimesh_scene()
        scene.export(scene_save_path)
        print("%d samples have been generated" % (sample_idx))
        
        
if __name__ == "__main__":
    main()
