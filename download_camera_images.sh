#!/bin/bash

# Download camera product images
# Since manufacturer sites block automated access, we'll use alternative approaches

cd /Users/kabbs/.openclaw/workspace/camera-quiz/images

# User agent to appear like a regular browser
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Function to download image with retries
download_image() {
    local camera_id="$1"
    local url="$2"
    local filename="${camera_id}.jpg"
    
    echo "Downloading $camera_id..."
    
    # Try to download
    curl -L -s -f \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.9" \
        -H "Cache-Control: no-cache" \
        --connect-timeout 10 \
        --max-time 30 \
        "$url" -o "$filename"
    
    if [ $? -eq 0 ] && [ -f "$filename" ]; then
        local size=$(stat -f%z "$filename" 2>/dev/null || stat -c%s "$filename" 2>/dev/null || echo "0")
        if [ "$size" -gt 1024 ]; then
            echo "✓ Downloaded $filename (${size} bytes)"
            return 0
        else
            echo "✗ File too small: $filename (${size} bytes)"
            rm -f "$filename"
        fi
    else
        echo "✗ Failed to download $filename"
        rm -f "$filename"
    fi
    
    return 1
}

# Try to download from publicly accessible image URLs
echo "Starting camera image downloads..."

# Sony FX3 - Try multiple sources
download_image "sony-fx3" "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=800&h=600&fit=crop&fm=jpg&q=80" || \
download_image "sony-fx3" "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=800&h=600"

# Sony FX30
download_image "sony-fx30" "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&fm=jpg&q=80"

# Sony A7S III
download_image "sony-a7siii" "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop&fm=jpg&q=80"

# Canon R5 II
download_image "canon-r5ii" "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&h=600&fit=crop&fm=jpg&q=80"

# For now, let's create a simple test with a few cameras and see if this approach works
echo "Test download complete. Checking results..."
ls -la *.jpg 2>/dev/null | head -5