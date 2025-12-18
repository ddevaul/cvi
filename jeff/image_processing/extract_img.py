import cv2
import numpy as np
import os
from pathlib import Path

def extract_and_save(image_path, output_dir = 'extracted'):

    # Create output directory
    Path(output_dir).mkdir(parents = True, exist_ok = True)
    
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Warning: Could not read {image_path}")
        return 0
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Color-based segmentation
    lower_bound = np.array([0, 30, 30])
    upper_bound = np.array([180, 255, 255])
    
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get base filename
    base_name = Path(image_path).stem
    
    saved_count = 0
    min_area = 5000
    for idx, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            illustration = img[y:y+h, x:x+w]

            output_path = os.path.join(output_dir, f"{base_name}_img_{idx:03d}_{w}x{h}.jpg")
            cv2.imwrite(output_path, illustration)
            saved_count += 1
    
    return saved_count


def process_folder(input_folder, output_dir = 'extracted'):
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp']
    min_area = 5000

    input_path = Path(input_folder)
    if not input_path.exists():
        print(f"Error: Folder '{input_folder}' does not exist!")
        return
    
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))
    
    image_files = sorted(list(set(image_files)))
    if not image_files:
        print(f"No image files found in '{input_folder}'")
        return
    
    total_illustrations = 0
    successful_pages = 0
    
    for i, img_path in enumerate(image_files, 1):
        
        count = extract_and_save(str(img_path), output_dir = output_dir)
        
        if count > 0:
            total_illustrations += count
            successful_pages += 1
            print(f"{count} found")
        else:
            print("None found")
    
process_folder(input_folder = 'voynich_pages', output_dir = 'voynich_extracted')