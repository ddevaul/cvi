import torch
from pathlib import Path
import shutil

# Load the pickle file (map to CPU if CUDA not available)
import pickle
with open('plant_images_plant_masks_scores.txt', 'rb') as f:
    # Use custom unpickler to handle nested torch objects
    class CPUUnpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'torch.storage' and name == '_load_from_bytes':
                return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
            return super().find_class(module, name)

    import io
    data = CPUUnpickler(f).load()

# Extract scores and sort by highest scores
# Assuming scores is a tensor, we'll take the max value or mean
scored_items = []
for page_id, scores in data:
    scores_cpu = scores.cpu() if scores.is_cuda else scores
    # Use max score for ranking (you can change to mean() if preferred)
    max_score = float(scores_cpu.max())
    scored_items.append((page_id, max_score))

# Sort by score in descending order and get top 100
scored_items.sort(key=lambda x: x[1], reverse=True)
top_100 = scored_items[:100]

print(f"Total items: {len(data)}")
print(f"Top 100 items selected\n")

# Create output folder for top 100 images
output_folder = Path("./top_100_images")
output_folder.mkdir(exist_ok=True)

# Source folder with images
image_folder = Path("/Users/darranshivdat/Downloads/voynich/plant_images_plant_cleaned")

# Copy top 100 files
copied_count = 0
for i, (page_id, score) in enumerate(top_100, 1):
    print(f"{i}. {page_id}: {score:.4f}")

    # Find the matching file in images folder
    # Try common naming patterns and extensions
    patterns = [
        f"{page_id}_cleaned.jpeg",
        f"{page_id}_cleaned.jpg",
        f"{page_id}.jpg",
        f"{page_id}.jpeg",
        f"{page_id}.png",
        f"{page_id}.webp"
    ]

    for pattern in patterns:
        src_file = image_folder / pattern
        if src_file.exists():
            # Keep original extension in output
            ext = src_file.suffix
            dst_file = output_folder / f"{i:03d}_{page_id}{ext}"
            shutil.copy2(src_file, dst_file)
            copied_count += 1
            break

print(f"\nCopied {copied_count} out of {len(top_100)} files to {output_folder}")
