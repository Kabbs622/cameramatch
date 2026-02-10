#!/usr/bin/env python3
"""
Download clean product images for camera quiz
This script attempts to find and download high-quality product images from various sources
"""

import requests
import os
import time
from urllib.parse import urlparse

# Set up headers to look like a regular browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Image sources - using publicly accessible URLs
CAMERA_IMAGES = {
    # Sony cameras
    'sony-fx3': [
        'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=800&h=600&fit=crop&crop=center',
        'https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=800&h=600'
    ],
    'sony-fx30': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'sony-a7siii': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    'sony-a7cii': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'sony-a7iv': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    'sony-zve10ii': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'sony-a6700': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    
    # Canon cameras  
    'canon-r5ii': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-r5c': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-r6iii': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-r7': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-r8': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-r50': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-c70': [
        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center',
    ],
    'canon-c80': [
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center',
    ],
    
    # Other cameras - using generic camera images for now
    'panasonic-s5iix': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'panasonic-s5ii': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'panasonic-gh7': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'panasonic-gh6': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'panasonic-g9ii': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    
    'blackmagic-cc6k': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'blackmagic-pocket4k': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'blackmagic-pocket6kg2': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'blackmagic-pyxis': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    
    'fujifilm-xh2s': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'fujifilm-xh2': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'fujifilm-xt5': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'fujifilm-xs20': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    
    'nikon-z6iii': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'nikon-z8': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'nikon-z50ii': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    
    'dji-osmo-pocket3': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
    'gopro-hero13': ['https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&crop=center'],
    'red-komodo': ['https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&crop=center'],
}

def download_image(camera_id, urls, target_dir):
    """Download image for a camera from the first working URL"""
    for i, url in enumerate(urls):
        try:
            print(f"Trying to download {camera_id} from URL {i+1}/{len(urls)}")
            
            response = requests.get(url, headers=HEADERS, timeout=10, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"  ⚠️  Not an image: {content_type}")
                continue
            
            # Save the image
            filename = os.path.join(target_dir, f"{camera_id}.jpg")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Check file size
            size = os.path.getsize(filename)
            if size > 1024:  # Must be larger than 1KB
                print(f"  ✓ Successfully downloaded {camera_id}.jpg ({size} bytes)")
                return True
            else:
                print(f"  ✗ Downloaded file too small ({size} bytes)")
                os.remove(filename)
                
        except Exception as e:
            print(f"  ✗ Error downloading from {url}: {e}")
            continue
    
    print(f"  ✗ Failed to download any image for {camera_id}")
    return False

def main():
    target_dir = "/Users/kabbs/.openclaw/workspace/camera-quiz/images"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    successful = 0
    failed = 0
    
    for camera_id, urls in CAMERA_IMAGES.items():
        if download_image(camera_id, urls, target_dir):
            successful += 1
        else:
            failed += 1
        
        # Be respectful with requests
        time.sleep(1)
    
    print(f"\n📊 Summary: {successful} successful, {failed} failed")

if __name__ == "__main__":
    main()