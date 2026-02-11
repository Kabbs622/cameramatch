#!/usr/bin/env python3
"""Merge Adorama + Amazon data into rigscout-master-data.csv"""
import csv
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load JSON data
with open('adorama-data.json') as f:
    adorama_raw = json.load(f)
adorama = {item['id']: item for item in adorama_raw}

with open('amazon-review-data.json') as f:
    amazon = json.load(f)

with open('amazon-affiliate-links.json') as f:
    affiliate = json.load(f)

# Read existing CSV
with open('rigscout-master-data.csv', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# Add new columns
new_cols = [
    'adorama_price', 'adorama_rating', 'adorama_review_count', 'adorama_in_stock',
    'amazon_rating', 'amazon_review_count',
    'amazon_affiliate_url',
    'avg_rating', 'total_review_count'
]
for col in new_cols:
    if col not in fieldnames:
        fieldnames.append(col)

# Merge data
for row in rows:
    cid = row['id']
    
    # Adorama data
    if cid in adorama:
        ad = adorama[cid]
        row['adorama_price'] = ad.get('adorama_price', '')
        row['adorama_rating'] = ad.get('adorama_rating', '')
        row['adorama_review_count'] = ad.get('adorama_review_count', '0')
        row['adorama_in_stock'] = ad.get('adorama_in_stock', '')
        # Update adorama link if we have a better one
        if ad.get('adorama_link'):
            row['adoramaLink'] = ad['adorama_link']
    
    # Amazon review data
    if cid in amazon:
        am = amazon[cid]
        row['amazon_rating'] = am.get('rating') if am.get('rating') is not None else ''
        row['amazon_review_count'] = am.get('reviewCount') if am.get('reviewCount') is not None else ''
    
    # Amazon affiliate URL
    if cid in affiliate:
        aff = affiliate[cid]
        row['amazon_affiliate_url'] = aff.get('affiliate_url', '')
        # Update the amazonLink column too
        row['amazonLink'] = aff['affiliate_url']
    
    # Calculate averaged rating across all 3 retailers
    ratings = []
    counts = []
    
    # B&H
    bh_r = row.get('bh_rating', '')
    if bh_r and bh_r != '':
        try:
            ratings.append(float(bh_r))
        except: pass
    bh_c = row.get('bh_review_count', '')
    if bh_c and bh_c != '':
        try:
            counts.append(int(bh_c))
        except: pass
    
    # Adorama
    ad_r = row.get('adorama_rating', '')
    if ad_r and ad_r != '':
        try:
            ratings.append(float(ad_r))
        except: pass
    ad_c = row.get('adorama_review_count', '0')
    if ad_c and ad_c != '' and ad_c != '0':
        try:
            counts.append(int(ad_c))
        except: pass
    
    # Amazon
    am_r = row.get('amazon_rating', '')
    if am_r and am_r != '':
        try:
            ratings.append(float(am_r))
        except: pass
    am_c = row.get('amazon_review_count', '')
    if am_c and am_c != '':
        try:
            counts.append(int(am_c))
        except: pass
    
    # Average rating (simple average across retailers that have ratings)
    if ratings:
        row['avg_rating'] = round(sum(ratings) / len(ratings), 2)
    else:
        row['avg_rating'] = ''
    
    # Total review count (sum across all retailers)
    row['total_review_count'] = sum(counts) if counts else ''

# Write merged CSV
with open('rigscout-master-data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Print summary
print("Merge complete!")
print(f"Total cameras: {len(rows)}")
print(f"Columns: {len(fieldnames)}")
print("\nSample data (first 5):")
for row in rows[:5]:
    print(f"  {row['id']}: avg={row['avg_rating']}, total_reviews={row['total_review_count']}, "
          f"bh={row.get('bh_rating','?')}/{row.get('bh_review_count','?')}, "
          f"adorama={row.get('adorama_rating','?')}/{row.get('adorama_review_count','?')}, "
          f"amazon={row.get('amazon_rating','?')}/{row.get('amazon_review_count','?')}")
