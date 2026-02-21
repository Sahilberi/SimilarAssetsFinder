🖼 iOS Asset Duplicate & Similarity Detector

A Python utility to detect duplicate and visually similar images inside an iOS .xcassets folder and generate a structured PDF report with image previews.

This tool helps reduce app size, remove redundant assets, and maintain a clean asset catalog.

🚀 Why This Tool?

In large iOS projects:

Multiple teams add assets over time

Same images get duplicated across different .imageset folders

Slightly renamed assets go unnoticed

App size increases unnecessarily

This script helps identify:

✅ Exact duplicates

✅ Visually similar images

✅ Cross-folder duplicates

🚫 Ignores valid 2x / 3x images inside same .imageset

📦 What This Project Does
1️⃣ Scans .xcassets Folder Recursively

Supports .png, .jpg, .jpeg

Walks through nested asset directories

2️⃣ Generates Perceptual Hash

Uses imagehash.phash

Detects visually similar images (not just identical files)

3️⃣ Smart iOS Handling

Ignores duplicates inside same .imageset
(to avoid false positives for @2x, @3x)

4️⃣ Compares Images

Uses Hamming distance for similarity score

Configurable similarity threshold

5️⃣ Generates PDF Report

The generated PDF includes:

Image 1 preview

Image 2 preview

Full file paths

Similarity distance score

🛠 Requirements

Python 3.8+

macOS / Linux / Windows

Install dependencies:
python3 -m pip install reportlab pillow imagehash
▶️ Usage
python3 asset_similarity_with_images_pdf.py /path/to/Assets.xcassets

Output:

Asset_Duplicate_Report_With_Images.pdf
📊 Similarity Threshold Guide
Distance	Meaning
0	Exact duplicate
1–5	Very similar
6–10	Possibly similar
>10	Different

You can modify this line in the script:

if distance <= 5:
🧠 How It Works

Compute perceptual hash (pHash) for each image

Compare hash values using Hamming distance

Skip images from same parent folder

Store matches

Generate PDF with image previews

🎯 Use Cases

Reduce IPA size

Clean legacy asset catalog

Pre-release asset audit

CI pipeline validation

App optimization before major release
