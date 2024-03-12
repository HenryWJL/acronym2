# Acronym++
[***Acronym***](https://github.com/NVlabs/acronym) dataset only contains single-object data, which is insufficient when cluttered environments are required. In this project, we extend ***Acronym*** to multi-object scenes using the methods suggested by the original authors. Follow the instructions below, you can create a custom dataset of your own.

## Requirements
```
pip install -r requirements.txt
```

## Usage
### Download
Download ***Acronym*** and ***ShapeNetSem*** datasets
- [ACRONYM](https://drive.google.com/file/d/1zcPARTCQx2oeiKk7a-wdN_CN-RUVX56c/view)
- [ShapeNetSem](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main)
### Install
Install and build ***Manifold***. Please follow the instructions on the web page.
- [Manifold](https://github.com/hjwdzh/Manifold)
### Customize Your Dataset
Modify `config/category.txt` to include whatever objects you want. Only the specified objects will appear in the generated dataset.
### Start Now
```bash
bash start.sh </.../acronym2> </.../Manifold> <where_h5> <where_obj> 0.02 10 1000 2000
```
```
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
### Other Options
1. You can use other supporting objects just by moving the meshes of objects into `supports` directory.
2. If you want to split the whole dataset into training, validation, and testing datasets, please refer to `train_val_test_split.py`. 
3. You can load "torch.Tensor" data from the generated dataset using `load_data.py`.
