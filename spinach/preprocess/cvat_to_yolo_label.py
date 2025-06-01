import xml.etree.ElementTree as ET
import os

# ==== Bạn tự thay đường dẫn tại đây ====
xml_path = r'C:\Users\tam\Documents\ML\CVAT1.1\Xb\annotations.xml'            # ← File annotation xuất từ CVAT
images_dir = r'C:\Users\tam\Documents\ML\OneDrive_3_31-5-2025\Xb'                  # ← Folder ảnh gốc (không dùng nhưng để check kích thước)
output_labels_dir = 'Xb_label'    # ← Folder muốn lưu file YOLO .txt

# ==== Tạo thư mục nếu chưa tồn tại ====
os.makedirs(output_labels_dir, exist_ok=True)

# ==== Parse XML ====
tree = ET.parse(xml_path)
root = tree.getroot()

image_data = {}

# Đọc từng ảnh trong file XML
for image in root.findall(".//image"):
    name = image.attrib['name']
    width = int(image.attrib['width'])
    height = int(image.attrib['height'])

    image_data[name] = {
        'size': (width, height),
        'groups': {}  # group_id → list of polygons
    }

    # Duyệt qua từng polygon
    for poly in image.findall("polygon"):
        points = poly.attrib['points']
        group_id = poly.attrib.get('group_id', None)

        if group_id is None:
            continue  # bỏ qua nếu không có group_id

        group_id = int(group_id)
        coords = []
        for pt in points.strip().split(";"):
            x, y = map(float, pt.split(","))
            coords.extend([x / width, y / height])  # chuyển sang tỉ lệ YOLO

        if group_id not in image_data[name]['groups']:
            image_data[name]['groups'][group_id] = []
        image_data[name]['groups'][group_id].append(coords)

# ==== Xuất ra file .txt YOLO segmentation ====
for name, info in image_data.items():
    output_path = os.path.join(output_labels_dir, os.path.splitext(name)[0] + ".txt")
    with open(output_path, "w") as f:
        for group_id, polygons in info['groups'].items():
            merged = []
            for poly in polygons:
                merged.extend(poly)
            f.write(f"0 {' '.join(map(str, merged))}\n")  # class_id = 0
