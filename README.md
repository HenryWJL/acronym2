# Acronym2
Extend Acronym dataset to multi-object scenes

## Usage
### Download
Download *Acronym* and *ShapeNetSem* datasets
- [ACRONYM](https://github.com/NVlabs/acronym)
- [ShapeNetSem](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main)
### Install
Install and build *Manifold*. Please follow the instructions on the web page below.
- [Manifold](https://github.com/hjwdzh/Manifold)
### Customize Your Dataset
Modify `config/category.txt` to include whatever objects you want. Only the specified objects will appear in the generated dataset.
### Start Now
```bash
bash process.sh </.../acronym2> </.../Manifold> <where_h5> <where_obj> 0.02 10 1000 2000

Arguments (in order):
    The absolute path of acronym2
    The absolute path of Manifold
    The absolute path of where you store downloaded grasp data (.h5 files)
    The absolute path of where you store downloaded mesh data (.obj files)
    A scaling ratio, depending on the supporting object itself
    The number of objects in a scene
    The number of grasps preserved in a scene
    The total number of samples in the generated dataset
```

