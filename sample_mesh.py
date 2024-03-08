import os
import sys
import argparse
import h5py
import random
from glob import glob


def make_parser():
    parser = argparse.ArgumentParser(
        description="Select object meshes from the specified categories.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--category",
        default="config/category.txt",
        help="The .txt file used for loading specified object categories."
    )
    parser.add_argument(
        "--object_dir",
        default="",
        help="The directory used for loading objects."
    )
    parser.add_argument(
        "--mesh_dir",
        default="",
        help="The directory used for loading meshes."
    )
    parser.add_argument(
        "--object_save_dir",
        default="",
        help="The directory used for storing sampled objects."
    )
    parser.add_argument(
        "--mesh_save_dir",
        default="",
        help="The directory used for storing sampled meshes."
    )
    parser.add_argument(
        "--num_sample",
        default=250,
        help="The number of meshes to sample."
    )
    return parser


def main(argv=sys.argv[1:]):
    parser = make_parser()
    args = parser.parse_args(argv)
    
    with open(args.category, 'r') as f:
        categories = f.readlines()
        
    print("=> Sampling...")
    # select objects from the specified categories
    object_paths = []
    for category in categories:
        object_path = os.path.join(args.object_dir, "%s_**.h5" % category.split('\n')[0])
        object_fnames = glob(object_path)
        object_paths.extend(object_fnames)
    # randomly sample objects
    assert args.num_sample <= len(object_paths), "Too many objects to sample!"
    object_paths = random.sample(object_paths, args.num_sample)
    # copy data    
    mesh_paths = glob(os.path.join(args.mesh_dir, "**.obj"))
    for object_path in object_paths:
        data = h5py.File(object_path, "r")
        mesh_fname = data["object/file"][()].decode('utf-8').split('/')[2]
        mesh_path = os.path.join(args.mesh_dir, mesh_fname)
        
        if mesh_path in mesh_paths:
            os.system(f'cp {object_path} {args.object_save_dir}')
            os.system(f'cp {mesh_path} {args.mesh_save_dir}')

    
if __name__ == '__main__':
    main()
