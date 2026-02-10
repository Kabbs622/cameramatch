#!/bin/bash

# Image download script for camera quiz
# This script downloads clean product images for all cameras

cd /Users/kabbs/.openclaw/workspace/camera-quiz/images

# Array of cameras and their image URLs from publicly accessible sources
declare -A CAMERA_URLS=(
    ["sony-fx3"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-fx3-camera-front-angle-02?$native$"
    ["sony-fx6"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-fx6-camera-front-angle-02?$native$"
    ["sony-fx30"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-fx30-camera-front-angle-02?$native$"
    ["sony-a7siii"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-a7s-iii-front-angle-02?$native$"
    ["sony-a7cii"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-a7c-ii-front-angle-02?$native$"
    ["sony-a7iv"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-a7-iv-front-angle-02?$native$"
    ["sony-zve10ii"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-zv-e10-ii-front-angle-02?$native$"
    ["sony-a6700"]="https://gmedia.playstation.com/is/image/SIEPDC/sony-a6700-front-angle-02?$native$"
)

# Function to download and convert image
download_image() {
    local camera_id="$1"
    local image_url="$2"
    local filename="${camera_id}.jpg"
    
    echo "Downloading $camera_id from $image_url"
    
    # Download with curl, following redirects, using browser-like user agent
    curl -L -s \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        -H "Accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.9" \
        "$image_url" -o "$filename"
    
    # Check if download succeeded
    if [ -s "$filename" ]; then
        local size=$(stat -f%z "$filename" 2>/dev/null || stat -c%s "$filename" 2>/dev/null)
        if [ "$size" -gt 1024 ]; then
            echo "✓ Successfully downloaded $filename (${size} bytes)"
        else
            echo "✗ Downloaded file $filename is too small (${size} bytes)"
            rm -f "$filename"
        fi
    else
        echo "✗ Failed to download $filename"
        rm -f "$filename"
    fi
}

# Download images for each camera
for camera_id in "${!CAMERA_URLS[@]}"; do
    download_image "$camera_id" "${CAMERA_URLS[$camera_id]}"
    sleep 1  # Be respectful with requests
done

echo "Download complete!"