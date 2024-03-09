# Acronym2
Extend Acronym dataset to multi-object scenes

## Usage
### Download
Download *Acronym* and *ShapeNetSem* datasets
- [ACRONYM](https://github.com/NVlabs/acronym)
- [ShapeNetSem](https://huggingface.co/datasets/ShapeNet/ShapeNetSem-archive/tree/main)
2. Install and build ***Manifold***
- [Manifold](https://github.com/hjwdzh/Manifold)
3. Customize `config/category.txt` to include whatever objects you want. Only the specified objects will appear in the multi-object scenes.
4. Start now:
```bash
bash process.sh </.../acronym2> </.../Manifold> <where_h5> <where_obj> 0.02 10 1000 2000
```

