# Getting Vehicle Damage Images for ClaimGuard

## Option 1: Roboflow Car Damage Dataset (Recommended - FREE)

1. **Create Roboflow Account** (Free):
   - Go to: https://universe.roboflow.com/
   - Sign up for free account

2. **Download Car Damage Dataset**:
   - Visit: https://universe.roboflow.com/car-damage-kadad/car-damage-images
   - Click "Download Dataset"
   - Select format: **"Folder Structure"** or **"COCO JSON"**
   - Download (300+ images, ~50MB)

3. **Extract to ClaimGuard**:
   ```bash
   # After downloading, extract to:
   unzip car-damage-images.zip -d data/raw/roboflow_damage/
   ```

4. **Link Images to Claims**:
   ```bash
   python scripts/link_roboflow_images.py
   ```

## Option 2: Free Stock Car Damage Images

Download from these free sources:

**Pexels (Free stock photos):**
- https://www.pexels.com/search/car%20damage/
- https://www.pexels.com/search/car%20accident/

**Pixabay:**
- https://pixabay.com/images/search/car%20damage/

**Unsplash:**
- https://unsplash.com/s/photos/car-damage

Save images to: `data/raw/sample_damage_images/`

## Option 3: Use Your Own Images

1. Place damage images in:
   ```
   data/raw/sample_damage_images/
   ```

2. Supported formats: JPG, PNG, WebP

3. Run linking script:
   ```bash
   python scripts/link_custom_images.py
   ```

## Option 4: VehiDE Dataset (Research Dataset - Large)

**Size:** 13,945 images (~5-10GB)
**Source:** Academic research paper
**Link:** https://www.tandfonline.com/doi/full/10.1080/24751839.2024.2367387

This is the full research dataset. For development, use Option 1 (Roboflow) instead.

## Quick Test with Single Image

Just want to test the damage analyzer?

1. Download any car damage image from Google Images
2. Save as: `data/raw/sample_damage_images/test.jpg`
3. Upload in the Gradio dashboard (Damage Assessment tab)

---

**Current Status:**
- ✅ 1 sample image linked to claim CLM-1994-000029
- 📁 Location: `data/raw/sample_damage_images/`

**Next Steps:**
1. Download images using one of the options above
2. View linked claims in dashboard
3. Upload new images for AI analysis
