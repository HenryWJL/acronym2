# Acronym++
This repository is adapted from [*Acronym*](https://github.com/NVlabs/acronym), a large-scale synthesized benchmark for grasp pose detection. In the original dataset, however, only samples of single object are provided, while diverse scenes with multiple objects are inaccessible. In this codebase, we provide users with several wrapped tools to synthesize hundreds of thousands of training and testing samples. By running a few lines of commands, you can easily generate your own custom dataset!

## Requirements
```
pip install -r requirements.txt
```

## Installation
### 1. Download Datasets
Download *Acronym* and *ShapeNet* datasets from web.
- [Acronym](https://drive.google.com/file/d/1zcPARTCQx2oeiKk7a-wdN_CN-RUVX56c/view)
- [ShapeNet](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main)
### 2. Build from Source
Follow the instructions in the codebase below to build *Manifold* from source.
- [Manifold](https://github.com/hjwdzh/Manifold)
### 3. Customize your Dataset
Modify `configs/category.txt` to include whatever objects you want. Only objects specified in this file will occur in your dataset.
### 4. Generate your Dataset
Now you can generate your own dataset just by running the following command.
```bash
bash start_pipeline.sh </**/acronym2> </**/Manifold> <h5_dir> <obj_dir> 0.02 10 1000 10000
```
```
Arguments:
    The absolute path of acronym2.
    The absolute path of Manifold.
    The absolute path of the directory where you store Acronym data (.h5).
    The absolute path of the directory where you store ShapeNet data (.obj).
    A scaling ratio of the supporting object.
    The number of objects per scene.
    The number of grasps per scene.
    The total number of samples.
```
### Other Options
1. If you want to use other supporting objects, just move the meshes of the supporting objects into `supports` directory.
2. If you want to split the whole dataset into training, validation, and testing sets, just run `scripts/train_val_test_split.py`. 
3. For data loading, refer to `scripts/load_data.py`.
