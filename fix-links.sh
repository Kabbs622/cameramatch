#!/bin/bash
# Scrape correct B&H links for all cameras using Firecrawl
API_KEY="fc-a5f89173f15d4fbca890e4656436268d"
OUTFILE="/Users/kabbs/.openclaw/workspace/camera-quiz/link-results.json"

echo "[" > "$OUTFILE"

cameras=(
  "sony-fx3|Sony FX3"
  "sony-fx6|Sony FX6"
  "sony-fx30|Sony FX30"
  "sony-a7siii|Sony A7S III"
  "sony-a7cii|Sony A7C II"
  "sony-a7iv|Sony A7 IV"
  "sony-zve10ii|Sony ZV-E10 II"
  "sony-a6700|Sony A6700"
  "canon-r5ii|Canon R5 Mark II"
  "canon-r5c|Canon R5 C"
  "canon-r6iii|Canon R6 Mark III"
  "canon-r7|Canon EOS R7"
  "canon-r8|Canon EOS R8"
  "canon-r50|Canon EOS R50"
  "canon-c70|Canon C70"
  "canon-c80|Canon C80"
  "panasonic-s5iix|Panasonic S5 IIX"
  "panasonic-s5ii|Panasonic S5 II"
  "panasonic-gh7|Panasonic GH7"
  "panasonic-gh6|Panasonic GH6"
  "panasonic-g9ii|Panasonic G9 II"
  "blackmagic-pocket4k|Blackmagic Pocket 4K"
  "blackmagic-pocket6kg2|Blackmagic Pocket 6K G2"
  "blackmagic-cc6k|Blackmagic Cinema Camera 6K"
  "blackmagic-pyxis|Blackmagic PYXIS 6K"
  "fujifilm-xh2s|Fujifilm X-H2S"
  "fujifilm-xh2|Fujifilm X-H2"
  "fujifilm-xt5|Fujifilm X-T5"
  "fujifilm-xs20|Fujifilm X-S20"
  "nikon-z6iii|Nikon Z6 III"
  "nikon-z8|Nikon Z8"
  "nikon-z50ii|Nikon Z50 II"
  "dji-osmo-pocket3|DJI Osmo Pocket 3"
  "gopro-hero13|GoPro HERO13 Black"
  "red-komodo|RED KOMODO 6K"
)

first=true
for entry in "${cameras[@]}"; do
  IFS='|' read -r id name <<< "$entry"
  echo "Searching B&H for: $name"
  
  # URL encode the search query
  query=$(echo "$name body" | sed 's/ /+/g')
  
  result=$(curl -s -X POST https://api.firecrawl.dev/v1/scrape \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://www.bhphotovideo.com/c/search?q=${query}\", \"formats\": [\"links\", \"markdown\"], \"onlyMainContent\": true}" 2>/dev/null)
  
  # Extract the first product link from markdown
  bh_link=$(echo "$result" | jq -r '.data.markdown' | grep -o 'https://www.bhphotovideo.com/c/product/[^)]*' | head -1)
  
  # Extract product image
  bh_image=$(echo "$result" | jq -r '.data.markdown' | grep -o 'https://static.bhphoto.com/images/images[0-9]*x[0-9]*/[^)]*\.jpg' | head -1)
  
  # Extract price
  bh_price=$(echo "$result" | jq -r '.data.markdown' | grep -oP '\$[\d,]+(?:\.\d{2})?' | head -1)
  
  if [ "$first" = true ]; then first=false; else echo "," >> "$OUTFILE"; fi
  echo "{\"id\":\"$id\",\"name\":\"$name\",\"bhLink\":\"$bh_link\",\"bhImage\":\"$bh_image\",\"bhPrice\":\"$bh_price\"}" >> "$OUTFILE"
  
  echo "  → B&H: $bh_link"
  echo "  → Image: $bh_image"
  echo "  → Price: $bh_price"
  
  sleep 1  # Rate limit
done

echo "]" >> "$OUTFILE"
echo "Done! Results in $OUTFILE"
