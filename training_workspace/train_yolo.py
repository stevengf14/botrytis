import os
import shutil
import random
import yaml
from ultralytics import YOLO

def repair_dataset_and_create_yaml(base_dir):
    """
    Verify dataset structure, create validation split if missing, and generate data.yaml.
    """
    # Check dataset structure
    
    train_img_dir = os.path.join(base_dir, 'train', 'images')
    train_lbl_dir = os.path.join(base_dir, 'train', 'labels')
    val_img_dir = os.path.join(base_dir, 'valid', 'images')
    val_lbl_dir = os.path.join(base_dir, 'valid', 'labels')

    # 1. Verify existence of training folder
    if not os.path.exists(train_img_dir):
        raise FileNotFoundError(f"Training images folder not found: {train_img_dir}")

    # 2. Verify or create validation folder (auto-split 20%)
    if not os.path.exists(val_img_dir) or len(os.listdir(val_img_dir)) == 0:
        print("Creating validation set (20% of train)...")
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(val_lbl_dir, exist_ok=True)

        images = [f for f in os.listdir(train_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        num_to_move = int(len(images) * 0.2)

        if num_to_move > 0:
            print(f"Moving {num_to_move} images to validation...")
            to_move = random.sample(images, num_to_move)

            for img_name in to_move:
                # Move image
                src_img = os.path.join(train_img_dir, img_name)
                dst_img = os.path.join(val_img_dir, img_name)
                shutil.move(src_img, dst_img)

                # Move label
                lbl_name = os.path.splitext(img_name)[0] + '.txt'
                src_lbl = os.path.join(train_lbl_dir, lbl_name)
                dst_lbl = os.path.join(val_lbl_dir, lbl_name)
                
                if os.path.exists(src_lbl):
                    shutil.move(src_lbl, dst_lbl)
            print("Validation set created successfully.")
        else:
            print("Warning: Not enough images to create validation.")

    # 3. Generate updated data.yaml
    yaml_content = {
        'path': base_dir.replace('\\', '/'),
        'train': 'train/images',
        'val': 'valid/images',
        'nc': 2,
        'names': ['botrytis_rose', 'uninfected_rose']
    }

    yaml_path = os.path.join(base_dir, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=None)
    
    print(f"Configuration file updated: {yaml_path}")
    return yaml_path

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(current_dir, 'dataset')

    try:
        yaml_path = repair_dataset_and_create_yaml(dataset_dir)
    except Exception as e:
        print(f"Critical error preparing dataset: {e}")
        return

    # Load and train
    print("Loading YOLOv8 Medium model...")
    model = YOLO('yolov8m.pt') 

    print("Starting training...")
    model.train(
        data=yaml_path,
        epochs=100,
        imgsz=512,
        patience=20,
        batch=8,
        name='rose_model_local',
        augment=True,
        project='runs/detect'
    )

    # Validate
    print("Validating final model...")
    metrics = model.val()
    print(f"Training finished. mAP50: {metrics.box.map50}")

if __name__ == '__main__':
    main()