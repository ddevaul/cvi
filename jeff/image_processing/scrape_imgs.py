import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO


def download_images(url, output_dir = 'downloaded_images', max_images = None):

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    try:
        # Send GET request
        print(f"Fetching webpage: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img_tags = soup.find_all('img')
        print(f"Found {len(img_tags)} image tags")
        
        if not img_tags:
            print("No images found on the page")
            return
        
        # Download images
        downloaded_count = 0
        for idx, img in enumerate(img_tags):
            if max_images and downloaded_count >= max_images:
                break
                
            # Get image URL
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue
            
            # Convert relative URLs to absolute
            img_url = urljoin(url, img_url)
            
            # Skip data URIs
            if img_url.startswith('data:'):
                continue
            
            try:
                # Download image
                print(f"Downloading image {downloaded_count + 1}: {img_url}")
                img_response = requests.get(img_url, headers=headers, timeout = 10)
                img_response.raise_for_status()
                
                # Generate filename (always use .jpg extension)
                parsed_url = urlparse(img_url)
                original_filename = os.path.basename(parsed_url.path)
                base_name = os.path.splitext(original_filename)[0] if original_filename else f"image_{idx + 1}"
                
                # If no base name, create one
                if not base_name:
                    base_name = f"image_{idx + 1}"
                
                filename = f"{base_name}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                # Handle duplicate filenames
                counter = 1
                while os.path.exists(filepath):
                    filename = f"{base_name}_{counter}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    counter += 1
                
                # Convert image to JPG format
                try:
                    img = Image.open(BytesIO(img_response.content))
                    
                    # Convert RGBA to RGB
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask = img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as JPG
                    img.save(filepath, 'JPEG', quality=95)
                    print(f"Saved as: {filename} (converted to JPG)")
                    downloaded_count += 1
                    
                except Exception as e:
                    print(f"Failed to convert image: {str(e)}")
                    continue
                
            except Exception as e:
                print(f"Failed to download {img_url}: {str(e)}")
                continue
        
        print(f"\nSuccessfully downloaded {downloaded_count} images to '{output_dir}'")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



if __name__ == '__main__':
    url = "https://publicdomainreview.org/collection/erbario-15th-century-herbal/"
    output = "erbario"
    max_n = 100
    
    download_images(url, output, max_n)
