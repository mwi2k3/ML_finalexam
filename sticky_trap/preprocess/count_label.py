import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import matplotlib.pyplot as plt

def count_labels_from_voc_xml(xml_dir):
    label_counts = defaultdict(int)

    for filename in os.listdir(xml_dir):
        if not filename.endswith(".xml"):
            continue
        path = os.path.join(xml_dir, filename)
        tree = ET.parse(path)
        root = tree.getroot()

        for obj in root.findall("object"):
            label = obj.find("name").text
            label_counts[label] += 1

    print("📊 Số lượng object theo từng class:")
    for label, count in label_counts.items():
        print(f"- {label}: {count}")

    return dict(label_counts)

label_counts = count_labels_from_voc_xml(r"C:\Users\tam\Documents\ML\yellow-sticky-traps-dataset-main\yellow-sticky-traps-dataset-main\annotations")

labels = list(label_counts.keys())
counts = list(label_counts.values())

plt.figure(figsize=(8, 6))
plt.bar(labels, counts, color='skyblue')
plt.title("Số lượng object theo từng class (VOC XML)")
plt.xlabel("Class")
plt.ylabel("Số lượng")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("label_distribution.png")
plt.show()
