"""
Download sample vehicle damage images and link them to claims
Uses public datasets and sample images for demonstration
"""

import requests
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def download_sample_images():
    """Download sample vehicle damage images from public sources"""

    print("📥 Downloading sample vehicle damage images...")
    print("="*60)

    images_dir = Path("data/raw/sample_damage_images")
    images_dir.mkdir(parents=True, exist_ok=True)

    # Sample public vehicle damage images (these are example URLs)
    # In production, you would use the VehiDE dataset or Roboflow
    sample_images = [
        {
            'url': 'https://images.unsplash.com/photo-1558980664-3a031cfcb5b4?w=800',
            'filename': 'damage_001.jpg',
            'description': 'Front bumper damage'
        },
        {
            'url': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800',
            'filename': 'damage_002.jpg',
            'description': 'Side panel dent'
        },
        {
            'url': 'https://images.unsplash.com/photo-1625255447829-feedf0d8d794?w=800',
            'filename': 'damage_003.jpg',
            'description': 'Rear collision'
        }
    ]

    downloaded = []

    for img in sample_images:
        try:
            print(f"\nDownloading: {img['filename']}")
            response = requests.get(img['url'], timeout=10)

            if response.status_code == 200:
                filepath = images_dir / img['filename']
                filepath.write_bytes(response.content)
                downloaded.append({
                    'filepath': str(filepath),
                    'filename': img['filename'],
                    'description': img['description']
                })
                print(f"✅ Saved: {filepath}")
            else:
                print(f"❌ Failed: HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Error downloading {img['filename']}: {e}")

    print("\n" + "="*60)
    print(f"✅ Downloaded {len(downloaded)} sample images")
    print(f"📁 Location: {images_dir}")

    return downloaded


def link_images_to_claims(image_files):
    """Link downloaded images to high-risk claims"""

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.core.config import settings
    from app.models.claim import Claim
    from app.models.fraud_score import FraudScore
    from app.models.damage_assessment import DamageAssessment, DamageType, DamageSeverity

    print("\n📎 Linking images to claims...")
    print("="*60)

    engine = create_engine(settings.DATABASE_URL)
    session = Session(engine)

    # Get some high-risk claims to link images to
    high_risk_claims = session.query(Claim).join(FraudScore).filter(
        FraudScore.fraud_score >= 0.6
    ).limit(len(image_files)).all()

    for idx, (claim, img_info) in enumerate(zip(high_risk_claims, image_files)):

        # Create damage assessment record
        assessment = DamageAssessment(
            claim_id=claim.id,
            file_url=img_info['filepath'],
            file_type='image',
            damage_type=DamageType.DENT,  # Default, will be updated by AI
            severity=DamageSeverity.MODERATE,
            severity_score=60,
            affected_areas=['front_bumper', 'hood'],
            estimated_cost_min=2000,
            estimated_cost_max=5000,
            ai_response='Sample image - pending AI analysis',
            model_version='pending',
            confidence_score=0.0,
            reviewed=False
        )

        session.add(assessment)
        print(f"✅ Linked {img_info['filename']} to claim {claim.claim_number}")

    session.commit()
    session.close()

    print("\n" + "="*60)
    print(f"✅ Successfully linked {len(image_files)} images to claims")
    print("\n💡 Next step: Run damage analysis on these images in the dashboard!")


if __name__ == "__main__":
    print("\n🛡️  ClaimGuard - Sample Image Downloader")
    print("="*60 + "\n")

    # Download images
    image_files = download_sample_images()

    if image_files:
        # Link to claims
        try:
            link_images_to_claims(image_files)
        except Exception as e:
            print(f"\n❌ Error linking images: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n⚠️  No images downloaded. Cannot link to claims.")
        print("\n📝 Alternative: You can manually place damage images in:")
        print("   data/raw/sample_damage_images/")
        print("   Then run this script to link them to claims.")
