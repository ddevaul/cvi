import fitz  # PyMuPDF
import cv2
import numpy as np
import os

output_dir = "extracted_images"
os.makedirs(output_dir, exist_ok=True)

pdf = fitz.open("Voynich.pdf")

# Extract and save images
for page_num in range(len(pdf)):
    page = pdf[page_num]
    images = page.get_images()
    
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = pdf.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        # Create filename
        filename = f"page{page_num + 1}.{image_ext}"
        filepath = os.path.join(output_dir, filename)
        
        # Save image
        with open(filepath, "wb") as img_file:
            img_file.write(image_bytes)
        
        print(f"Saved: {filepath}")

pdf.close()

'''
Extracts images from pdf at ~1500x2000 (~500KB) per image, where high res are available at ~2900x3800 (~2MB) 
'''

