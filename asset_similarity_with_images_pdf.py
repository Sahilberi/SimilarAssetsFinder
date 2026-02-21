import os
import sys
from PIL import Image
import imagehash

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

# ----------------------------
# Argument Check
# ----------------------------
if len(sys.argv) != 2:
    print("Usage: python3 asset_similarity_with_images_pdf.py /path/to/Assets.xcassets")
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.isdir(folder_path):
    print("Invalid folder path")
    sys.exit(1)

output_pdf = "Asset_Duplicate_Report_With_Images.pdf"

valid_extensions = (".png", ".jpg", ".jpeg")
image_hashes = {}

# ----------------------------
# Generate perceptual hashes
# ----------------------------
for root, _, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith(valid_extensions):
            full_path = os.path.join(root, file)
            try:
                with Image.open(full_path) as img:
                    phash = imagehash.phash(img)

                image_hashes[full_path] = {
                    "hash": phash,
                    "folder": os.path.dirname(full_path)
                }
            except Exception:
                pass

# ----------------------------
# Compare images
# ----------------------------
results = []
files = list(image_hashes.keys())

for i in range(len(files)):
    for j in range(i + 1, len(files)):
        file1 = files[i]
        file2 = files[j]

        folder1 = image_hashes[file1]["folder"]
        folder2 = image_hashes[file2]["folder"]

        # Ignore same folder (2x/3x case)
        if folder1 == folder2:
            continue

        distance = image_hashes[file1]["hash"] - image_hashes[file2]["hash"]

        if distance <= 5:
            results.append((file1, file2, distance))

# ----------------------------
# Generate PDF
# ----------------------------
doc = SimpleDocTemplate(output_pdf, pagesize=A4)
elements = []
styles = getSampleStyleSheet()

elements.append(Paragraph("<b>Asset Duplicate / Similarity Report</b>", styles["Title"]))
elements.append(Spacer(1, 0.4 * inch))

if not results:
    elements.append(Paragraph("No duplicate or similar images found.", styles["Normal"]))
else:
    for file1, file2, distance in results:

        elements.append(Paragraph(f"<b>Similarity Distance:</b> {distance}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph(f"<b>Image 1:</b> {file1}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        img1 = RLImage(file1, width=2.5 * inch, height=2.5 * inch, kind='proportional')
        elements.append(img1)
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph(f"<b>Image 2:</b> {file2}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        img2 = RLImage(file2, width=2.5 * inch, height=2.5 * inch, kind='proportional')
        elements.append(img2)
        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Spacer(1, 0.5 * inch))

doc.build(elements)

print("✅ PDF generated:", output_pdf)
