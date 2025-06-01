import os
import cv2
import numpy as np
import random
from tqdm import tqdm
import shutil

def add_salt_pepper_noise(image, amount=0.005):
    noisy = image.copy()
    num_salt = np.ceil(amount * image.size * 0.5).astype(int)
    num_pepper = np.ceil(amount * image.size * 0.5).astype(int)

    # Add salt
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    noisy[coords[0], coords[1]] = 255

    # Add pepper
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    noisy[coords[0], coords[1]] = 0

    return noisy

def change_brightness(image, factor_range=(0.85, 1.15)):
    factor = random.uniform(*factor_range)
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def augment_into_same_folder(image_dir, label_dir, noise_ratio=0.005):
    for filename in tqdm(os.listdir(image_dir)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        name, ext = os.path.splitext(filename)
        img_path = os.path.join(image_dir, filename)
        label_path = os.path.join(label_dir, name + '.txt')

        # Bỏ qua nếu không có label
        if not os.path.exists(label_path):
            print(f"⚠️ Không có label cho {filename}")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ Không đọc được ảnh {img_path}")
            continue

        # Augmentation
        bright_img = change_brightness(img)
        noisy_img = add_salt_pepper_noise(bright_img, amount=noise_ratio)

        # Tên mới
        new_img_name = f"{name}_aug.jpg"
        new_label_name = f"{name}_aug.txt"

        # Lưu ảnh và label
        cv2.imwrite(os.path.join(image_dir, new_img_name), noisy_img)
        shutil.copy(label_path, os.path.join(label_dir, new_label_name))

if __name__ == "__main__":
    augment_into_same_folder(
        image_dir=r"C:\Users\tam\Documents\ML\leaf_dataset_grouped_31_05\images\test",
        label_dir=r"C:\Users\tam\Documents\ML\leaf_dataset_grouped_31_05\labels\test",
        noise_ratio=0.005
    )