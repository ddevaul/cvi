from kindwise import PlantApi
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

API_KEY = "YOUR_KINDWISE_API_KEY"
api = PlantApi(api_key=API_KEY)

image_folder = Path("./top_100_images")
output_folder = Path("./top_100_results")
output_folder.mkdir(exist_ok=True)

for img_path in image_folder.glob("*"):
    if img_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        print(f"\n{img_path.name}")
        
        result = api.identify(str(img_path), details=["common_names", "image"])
        
        top = result.result.classification.suggestions[0]
        print(f"  → {top.name} ({top.probability:.1%})")
        
        if top.details.get("image"):
            img_url = top.details["image"]["value"]
            img_data = requests.get(img_url).content

            original_img = Image.open(img_path)
            reference_img = Image.open(BytesIO(img_data))

            target_height = 800
            original_ratio = original_img.width / original_img.height
            reference_ratio = reference_img.width / reference_img.height

            original_resized = original_img.resize((int(target_height * original_ratio), target_height), Image.LANCZOS)
            reference_resized = reference_img.resize((int(target_height * reference_ratio), target_height), Image.LANCZOS)

            total_width = original_resized.width + reference_resized.width
            combined = Image.new('RGB', (total_width, target_height))

            combined.paste(original_resized, (0, 0))
            combined.paste(reference_resized, (original_resized.width, 0))

            draw = ImageDraw.Draw(combined)
            text = f"{top.name} - {top.probability:.1%} match"

            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            padding = 20
            text_x = (total_width - text_width) // 2
            text_y = target_height - text_height - padding

            bg_padding = 10
            draw.rectangle(
                [text_x - bg_padding, text_y - bg_padding,
                 text_x + text_width + bg_padding, text_y + text_height + bg_padding],
                fill=(0, 0, 0, 180)
            )

            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

            safe_name = top.name.replace(" ", "_")
            out_path = output_folder / f"{img_path.stem}_{safe_name}.jpg"
            combined.save(out_path, quality=95)
            print(f"  Saved: {out_path}")
            