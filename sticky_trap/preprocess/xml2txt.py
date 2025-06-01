import os
import xml.etree.ElementTree as ET
from PIL import Image

def convert_voc_to_yolo(xml_folder, img_folder, out_folder, class_list):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith('.xml'):
            continue
        tree = ET.parse(os.path.join(xml_folder, xml_file))
        root = tree.getroot()
        filename = xml_file.replace('.xml', '.jpg')
        img_path = os.path.join(img_folder, filename)
        img = Image.open(img_path)
        img_w, img_h = img.size

        yolo_lines = []
        for obj in root.findall('object'):
            cls = obj.find('name').text
            if cls not in class_list:
                continue
            cls_id = class_list.index(cls)

            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymin = int(xmlbox.find('ymin').text)
            ymax = int(xmlbox.find('ymax').text)

            x_center = (xmin + xmax) / 2.0 / img_w
            y_center = (ymin + ymax) / 2.0 / img_h
            w = (xmax - xmin) / img_w
            h = (ymax - ymin) / img_h

            yolo_lines.append(f"{cls_id} {x_center} {y_center} {w} {h}")

        out_txt = os.path.join(out_folder, xml_file.replace('.xml', '.txt'))
        with open(out_txt, 'w') as f:
            f.write('\n'.join(yolo_lines))

# Ví dụ sử dụng
classes = ["MR", "NC", "WF", "TR"]  # sửa theo class của bạn
convert_voc_to_yolo("yellow-sticky-traps-dataset-main/yellow-sticky-traps-dataset-main/annotations", "yellow-sticky-traps-dataset-main/yellow-sticky-traps-dataset-main/images", "labels_yolo", classes)
