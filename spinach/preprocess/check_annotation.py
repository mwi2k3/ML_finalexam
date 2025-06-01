import os
import cv2
import xml.etree.ElementTree as ET

# CẤU HÌNH: chỉnh lại đường dẫn phù hợp với thư mục của bạn
image_folder = r'C:\Users\tam\Documents\ML\yellow-sticky-traps-dataset-main\yellow-sticky-traps-dataset-main\images'   # Thư mục ảnh
xml_folder = r'C:\Users\tam\Documents\ML\yellow-sticky-traps-dataset-main\yellow-sticky-traps-dataset-main\annotations'     # Thư mục chứa XML

# Tạo cửa sổ để xem ảnh
cv2.namedWindow('Annotation Viewer', cv2.WINDOW_NORMAL)

# Duyệt qua từng ảnh
for file in os.listdir(image_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        basename = os.path.splitext(file)[0]
        image_path = os.path.join(image_folder, file)
        xml_path = os.path.join(xml_folder, basename + '.xml')

        # Đọc ảnh
        img = cv2.imread(image_path)
        if img is None:
            print(f"[!] Không đọc được ảnh: {image_path}")
            continue

        h, w = img.shape[:2]

        # Kiểm tra file XML
        if not os.path.exists(xml_path):
            print(f"[!] Không tìm thấy XML tương ứng với ảnh: {file}")
            continue

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for obj in root.findall('object'):
                name = obj.find('name').text
                bndbox = obj.find('bndbox')
                # Clamp box tọa độ
                xmin = max(0, int(float(bndbox.find('xmin').text)))
                ymin = max(0, int(float(bndbox.find('ymin').text)))
                xmax = min(w - 1, int(float(bndbox.find('xmax').text)))
                ymax = min(h - 1, int(float(bndbox.find('ymax').text)))

                box_width = xmax - xmin
                box_height = ymax - ymin

                # Bỏ qua box sai
                if box_width <= 0 or box_height <= 0:
                    print(f"[!] Box lỗi: ({xmin}, {ymin}, {xmax}, {ymax})")
                    continue

                # Tăng nét nếu box nhỏ
                thickness = max(2, min(5, box_width // 10))

                # Vẽ box
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), thickness)
                cv2.putText(img, name, (xmin, max(0, ymin - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

                # Gắn label nếu box nhỏ bất thường
                if box_width < 4 or box_height < 4:
                    cv2.putText(img, 'small box', (xmin, ymax + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            # Hiển thị ảnh
            cv2.imshow('Annotation Viewer', img)
            key = cv2.waitKey(0)
            if key == ord('q'):
                break

        except Exception as e:
            print(f"[!] Lỗi đọc file XML {basename}.xml: {e}")

cv2.destroyAllWindows()
