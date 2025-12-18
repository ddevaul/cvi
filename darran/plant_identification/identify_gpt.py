import base64
import os
from pathlib import Path
from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def identify_plant(image_path):
    b64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a botanical expert analyzing historical manuscript illustrations. Provide concise scientific identifications without explanations."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":  "Describe the morphological features of this plant illustration, including root structure, leaf arrangement, stem characteristics, and any flowering or fruiting bodies." "Compare this illustration to known medieval herbal manuscript traditions. What real plants might this represent? What stylistic traditions does it follow?" "Identify any unusual or fantastical elements in this botanical illustration that deviate from naturalistic plant representation."

                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
                    }
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

image_folder = Path("./top_100_images")
output_file = Path("./voynich_gpt_identifications.json")
results = {}

if output_file.exists():
    with open(output_file, "r") as f:
        results = json.load(f)
    print(f"Loaded {len(results)} existing results. Resuming...")

image_files = sorted(image_folder.glob("*.jpeg"))[:50]

for img_path in image_files:
    if img_path.name in results:
        print(f"Skipping {img_path.name} (already processed)")
        continue

    print(f"\nProcessing {img_path.name}...")
    try:
        results[img_path.name] = identify_plant(img_path)
        print(results[img_path.name])
        print("-" * 80)

        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error processing {img_path.name}: {e}")
        results[img_path.name] = f"ERROR: {str(e)}"

print(f"\n✓ Complete! Processed {len(results)} images.")
print(f"Results saved to: {output_file}")
