import os
import shutil
import random
import yaml
from ultralytics import YOLO

def repair_dataset_and_create_yaml(base_dir):
    """
    Verifica si existe carpeta de validación. Si no, toma el 20% de train.
    Luego genera un data.yaml con rutas absolutas para evitar errores.
    """
    print(f"Verificando estructura del dataset en: {base_dir}")
    
    train_img_dir = os.path.join(base_dir, 'train', 'images')
    train_lbl_dir = os.path.join(base_dir, 'train', 'labels')
    val_img_dir = os.path.join(base_dir, 'valid', 'images')
    val_lbl_dir = os.path.join(base_dir, 'valid', 'labels')

    # 1. Verificar si existe train
    if not os.path.exists(train_img_dir):
        # Intento de corrección: A veces las carpetas se llaman solo 'train' sin subcarpeta 'images'
        # Si tu estructura es dataset/train/*.jpg, ajusta aquí. 
        # Pero asumiendo estructura YOLO estándar (train/images):
        raise FileNotFoundError(f"No encuentro la carpeta de entrenamiento en: {train_img_dir}")

    # 2. Verificar/Crear Validación
    # Si la carpeta no existe o está vacía, hacemos el split
    if not os.path.exists(val_img_dir) or len(os.listdir(val_img_dir)) == 0:
        print("No se encontró set de validación (o está vacío). Creándolo automáticamente...")
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(val_lbl_dir, exist_ok=True)

        # Listar imágenes
        images = [f for f in os.listdir(train_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        num_to_move = int(len(images) * 0.2)  # 20%

        if num_to_move > 0:
            print(f"Moviendo {num_to_move} imágenes de 'train' a 'valid'...")
            to_move = random.sample(images, num_to_move)

            for img_name in to_move:
                # Mover Imagen
                src_img = os.path.join(train_img_dir, img_name)
                dst_img = os.path.join(val_img_dir, img_name)
                shutil.move(src_img, dst_img)

                # Mover Label (si existe)
                # Asumimos que el label tiene el mismo nombre pero termina en .txt
                lbl_name = os.path.splitext(img_name)[0] + '.txt'
                src_lbl = os.path.join(train_lbl_dir, lbl_name)
                dst_lbl = os.path.join(val_lbl_dir, lbl_name)
                
                if os.path.exists(src_lbl):
                    shutil.move(src_lbl, dst_lbl)
            print("Validación creada exitosamente.")
        else:
            print("Muy pocas imágenes para dividir. Se usará lo que haya.")
    else:
        print("Carpeta de validación encontrada y con datos.")

    # 3. Generar data.yaml con rutas ABSOLUTAS (Vital para Windows/Linux)
    # Usamos barras '/' que funcionan universalmente en rutas de Python/YOLO
    yaml_content = {
        'path': base_dir.replace('\\', '/'),
        'train': 'train/images',
        'val': 'valid/images',
        'nc': 2,
        'names': ['botrytis_rose', 'healthy_rose']
    }

    yaml_path = os.path.join(base_dir, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=None)
    
    print(f"📝 Archivo de configuración actualizado en: {yaml_path}")
    return yaml_path

def main():
    # 1. Definir rutas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(current_dir, 'dataset') # La carpeta se llama 'dataset'

    # 2. Reparar dataset y obtener yaml
    try:
        yaml_path = repair_dataset_and_create_yaml(dataset_dir)
    except Exception as e:
        print(f"Error preparando el dataset: {e}")
        return

    # 3. Cargar Modelo (Medium)
    print("Cargando modelo YOLOv8 Medium...")
    model = YOLO('yolov8m.pt') 

    # 4. Entrenar
    print("Iniciando entrenamiento...")
    model.train(
        data=yaml_path,
        epochs=100,
        imgsz=640,
        patience=20,
        batch=8,           # Mantener en 8 (subir a 16 si se tiene una buena GPU)
        name='modelo_rosas_local',
        augment=True,      # Data augmentation activado
        project='runs/detect' # Guardar resultados organizados localmente
    )

    # 5. Validar
    print("Validando modelo final...")
    metrics = model.val()
    print(f"Entrenamiento finalizado. mAP50: {metrics.box.map50}")

if __name__ == '__main__':
    main()