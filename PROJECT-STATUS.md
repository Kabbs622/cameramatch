# RigScout — Project Status

## Scraping / Data Collection

### Goal
Scrape B&H, Amazon, and Adorama for all 35 cameras to collect:
- Current price
- Review rating (stars)
- Review count
- In-stock status
- Product image URL
- Buy link (verified correct product)

Then average reviews across all 3 retailers for a combined score on each camera.

### B&H — ✅ DONE
- Scraped via Firecrawl API
- Data in: `bh-cameras.csv` (name, SKU, URL, image)
- Also merged into `rigscout-master-data.csv` with columns: `bh_current_price`, `bh_list_price`, `bh_savings`, `bh_rating`, `bh_review_count`, `bh_in_stock`, `bh_sku`, `bh_image_500`, etc.
- 35 cameras covered

### Adorama — 🟡 PARTIAL
- Data in: `adorama-data.json`
- Has: price, rating, review count, in-stock, link
- Some cameras returned 404 (e.g., Sony FX3A)
- Needs review to confirm all links point to correct products

### Amazon — ❌ NOT STARTED
- Need to scrape Amazon product pages for each camera
- Collect: price, rating, review count, buy link
- Amazon links exist in `rigscout-master-data.csv` (`amazonLink` column) but haven't been verified or scraped
- Firecrawl may have trouble with Amazon (anti-bot protections) — may need alternative approach

### Master Spreadsheet
- `rigscout-master-data.csv` — 36 rows (header + 35 cameras)
- Contains all B&H data merged in
- Adorama data in separate `adorama-data.json` (not yet merged into master CSV)
- Amazon data not yet collected

### Next Steps
1. **Scrape Amazon** — get price, rating, review count for all 35 cameras
2. **Merge Adorama data** into master CSV
3. **Merge Amazon data** into master CSV
4. **Calculate average review scores** across all 3 retailers
5. **Verify all buy links** point to correct products (known issue: some B&H links in `link-results.json` are wrong, e.g., FX3 points to an AquaTech housing)
6. **Update `index.html`** with corrected links, prices, and averaged ratings

## Other Files
- `link-results.json` — early B&H link scrape (some links are WRONG, superseded by master CSV)
- `photo-results.json` — product photo scrape results
- `fix-links.sh` — script for fixing links
- `images/` — local product images

## Tools
- **Firecrawl API** for scraping (key at `~/.openclaw/workspace/.firecrawl-key`)
- Firecrawl job ID from Kyle: `fc-a5f89173f15d4fbca890e4656436268d`

## Site Info
- Live: `rigscout.c41cinema.com`
- Repo: `Kabbs622/rigscout` on GitHub Pages
- Single-page app: `index.html` (~2050 lines, all inline JS/CSS/data)

---
*Last updated: 2026-02-10*
