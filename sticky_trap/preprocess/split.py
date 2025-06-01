import os
import shutil
import random

# Đường dẫn tới ảnh và nhãn gốc
IMG_DIR = "yellow-sticky-traps-dataset-main\yellow-sticky-traps-dataset-main\images"         # ảnh: 0001.jpg, 0002.jpg,...
LABEL_DIR = "labels_yolo"  # nhãn YOLO: 0001.txt, 0002.txt,...

# Thư mục đích
OUT_DIR = "dataset"
splits = ['train', 'val', 'test']
for split in splits:
    os.makedirs(os.path.join(OUT_DIR, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(OUT_DIR, 'labels', split), exist_ok=True)

# Tỉ lệ chia
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Lấy danh sách file ảnh
all_images = [f for f in os.listdir(IMG_DIR) if f.endswith(('.jpg', '.png'))]
random.shuffle(all_images)

# Tính số lượng
total = len(all_images)
train_count = int(train_ratio * total)
val_count = int(val_ratio * total)

train_files = all_images[:train_count]
val_files = all_images[train_count:train_count + val_count]
test_files = all_images[train_count + val_count:]

# Hàm copy ảnh và nhãn tương ứng
def copy_data(file_list, split_name):
    for file in file_list:
        base = os.path.splitext(file)[0]
        img_src = os.path.join(IMG_DIR, file)
        label_src = os.path.join(LABEL_DIR, base + ".txt")

        img_dst = os.path.join(OUT_DIR, 'images', split_name, file)
        label_dst = os.path.join(OUT_DIR, 'labels', split_name, base + ".txt")

        shutil.copy(img_src, img_dst)
        if os.path.exists(label_src):
            shutil.copy(label_src, label_dst)

# Thực hiện chia
copy_data(train_files, 'train')
copy_data(val_files, 'val')
copy_data(test_files, 'test')

print(f"Tổng ảnh: {total} | Train: {len(train_files)} | Val: {len(val_files)} | Test: {len(test_files)}")
