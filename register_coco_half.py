import os

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import load_coco_json
from detectron2.data.datasets.builtin_meta import COCO_CATEGORIES, _get_coco_instances_meta


### Register subsampled COCO train dataset
# - For training use a sample of 50% LVIS images and all available COCO annotations for them
# - For validation use images that appear in both COCO and LVIS validation split (only ~200 images removed from the
#   default COCO val split) and all available COCO annotations for them
#
# For implementation reference see:
# - register_all_coco(): https://github.com/facebookresearch/detectron2/blob/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/detectron2/data/datasets/builtin.py#L106
# - register_coco_instances(): https://github.com/facebookresearch/detectron2/blob/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/detectron2/data/datasets/coco.py#L479

_root = os.getenv("DETECTRON2_DATASETS", "datasets")

# COCO 2017 train dataset with only 50% of images kept
json_path_train = os.path.join(_root, "coco/annotations/coco_half_train.json")
image_root_train = os.path.join(_root, "coco/train2017")

json_path_val = os.path.join(_root, "coco/annotations/coco_half_val.json")
image_root_val = os.path.join(_root, "coco/val2017")

coco_meta = _get_coco_instances_meta()

# Check if the datasets were registered already (this may happen due to multiple imports in downstream files)
try:
    DatasetCatalog.get("coco_half_train")
except:
    DatasetCatalog.register(
        name="coco_half_train",
        func=lambda: load_coco_json(
            json_file=json_path_train,
            image_root=image_root_train,
            dataset_name="coco_half_train"
        )
    )
    MetadataCatalog.get("coco_half_train").set(
        json_file=json_path_train, image_root=image_root_train, evaluator_type="coco", **coco_meta
    )

    DatasetCatalog.register(
        name="coco_half_val",
        func=lambda: load_coco_json(
            json_file=json_path_val,
            image_root=image_root_val,
            dataset_name="coco_half_val"
        )
    )
    MetadataCatalog.get("coco_half_val").set(
        json_file=json_path_val, image_root=image_root_val, evaluator_type="coco", **coco_meta
    )
