# acronym_2.0
Extend Acronym dataset to multi-object scenes

## Usage
1. Download ***Acronym*** and ***ShapeNetSem***
- [ACRONYM](https://github.com/NVlabs/acronym)
- [ShapeNetSem](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main)
2. Install and build ***Manifold***
- [Manifold](https://github.com/hjwdzh/Manifold)
3. Customize `config/category.txt` to include whatever objects you want. Thereafter, sample the objects from datasets:
```python
python sample_mesh.py --object_dir <where_hdf5_are_stored> --mesh_dir <where_obj_are_stored> --object_save_dir <...> --mesh_save_dir <...>
```
4. Transform meshes into simplified watertight versions. Modify the paths in `process.sh` and run:
```bash
bash process.sh </.../acronym2> </.../Manifold> <where_.h5> <where_.obj>
```
5. Generate multi-object scenes:
```python
python generate_scene.py
```
6. Split the dataset into training, validation, and testing sets (Optional):
```python
python train_val_test_split.py
```
