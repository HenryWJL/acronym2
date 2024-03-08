import os
import sys
import random
import argparse
import h5py
from glob import glob


def make_parser():
    parser = argparse.ArgumentParser(
        description="Split the dataset into training, validation, and testing datasets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--object_dir",
        default="../data/grasps/objects",
        help="The directory used for loading objects."
    )
    parser.add_argument(
        "--mesh_dir",
        default="../data/meshes/objects",
        help="The directory used for loading objects' meshes."
    )
    parser.add_argument(
        "--ratio",
        nargs="+",
        type=int,
        help="The ratio used for splitting the dataset.",
    )
    return parser


def main(argv=sys.argv[1:]):
    parser = make_parser()
    args = parser.parse_args(argv)
    
    object_train_dir = os.path.join(args.object_dir, "train")
    object_val_dir = os.path.join(args.object_dir, "val")
    object_test_dir = os.path.join(args.object_dir, "test")
    mesh_train_dir = os.path.join(args.mesh_dir, "train")
    mesh_val_dir = os.path.join(args.mesh_dir, "val")
    mesh_test_dir = os.path.join(args.mesh_dir, "test")
    
    if not os.path.exists(object_train_dir):
        os.mkdir(object_train_dir)
        
    if not os.path.exists(object_val_dir):
        os.mkdir(object_val_dir)
        
    if not os.path.exists(object_test_dir):
        os.mkdir(object_test_dir)
        
    if not os.path.exists(mesh_train_dir):
        os.mkdir(mesh_train_dir)
        
    if not os.path.exists(mesh_val_dir):
        os.mkdir(mesh_val_dir)
        
    if not os.path.exists(mesh_test_dir):
        os.mkdir(mesh_test_dir)
        
    # load and shuffle the objects
    objects = glob(os.path.join(args.object_dir, "**.h5"))
    random.shuffle(objects)
    # split the objects into training, validation, and testing datasets
    num_train = len(objects) // (args.ratio[0] + args.ratio[1] + args.ratio[2]) * args.ratio[0]
    num_val = len(objects) // (args.ratio[0] + args.ratio[1] + args.ratio[2]) * args.ratio[1]
    objects_train = objects[: num_train]
    objects_val = objects[num_train: (num_train + num_val)]
    objects_test = objects[(num_train + num_val): ]
    # copy data
    for o in objects_train:
        data = h5py.File(o, "r")
        mesh_fname = data["object/file"][()].decode('utf-8').split('/')[2]
        mesh = os.path.join(args.mesh_dir, mesh_fname)
        os.system(f'cp {o} {object_train_dir}')
        os.system(f'cp {mesh} {mesh_train_dir}')
        
    for o in objects_val:
        data = h5py.File(o, "r")
        mesh_fname = data["object/file"][()].decode('utf-8').split('/')[2]
        mesh = os.path.join(args.mesh_dir, mesh_fname)
        os.system(f'cp {o} {object_val_dir}')
        os.system(f'cp {mesh} {mesh_val_dir}')
        
    for o in objects_test:
        data = h5py.File(o, "r")
        mesh_fname = data["object/file"][()].decode('utf-8').split('/')[2]
        mesh = os.path.join(args.mesh_dir, mesh_fname)
        os.system(f'cp {o} {object_test_dir}')
        os.system(f'cp {mesh} {mesh_test_dir}')


if __name__ == "__main__":
    main()
