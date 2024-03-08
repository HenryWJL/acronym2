# acronym_2.0
Extend Acronym dataset to multi-object scenes

## Usage
1. Download [ACRONYM](https://github.com/NVlabs/acronym).
2. Download [ShapeNetSem](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main).
3. Sample objects from specified categories. You can customize `category.txt` to include the objects you want.
```python
cd dataset
python sample_mesh.py
```
4. Generate and simplify the watertight versions of the meshes. Note that the process may sometimes fail when simplifying meshes, which would cause outliers. To handle these outliers, we simply remove them. Here we provide a shell script to complete the aforementioned procedures. Please open the script and modify the paths before running the following command.
```bash
bash postprocess.sh
```
5. Generate scenes.
```python
python generate_scene.py
```
6. Split the dataset (Optional)
```python
python train_val_test_split.py
```
