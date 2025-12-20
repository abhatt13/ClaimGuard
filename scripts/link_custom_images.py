"""
Link custom damage images from data/raw/sample_damage_images/ to claims
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.models.claim import Claim
from app.models.fraud_score import FraudScore
from app.models.damage_assessment import DamageAssessment, DamageType, DamageSeverity


def link_custom_images():
    """Link all images in sample_damage_images to high-risk claims"""

    images_dir = Path("data/raw/sample_damage_images")

    if not images_dir.exists():
        print(f"❌ Directory not found: {images_dir}")
        print("\nCreate it with: mkdir -p data/raw/sample_damage_images")
        return

    # Find all image files
    image_files = list(images_dir.glob("*.jpg")) + \
                  list(images_dir.glob("*.jpeg")) + \
                  list(images_dir.glob("*.png")) + \
                  list(images_dir.glob("*.webp"))

    if not image_files:
        print(f"❌ No images found in {images_dir}")
        print("\nAdd some images first:")
        print("1. Download car damage images")
        print(f"2. Save them to: {images_dir}")
        print("3. Run this script again")
        return

    print(f"\n📸 Found {len(image_files)} images")
    print("="*60)

    engine = create_engine(settings.DATABASE_URL)
    session = Session(engine)

    # Get high-risk claims without existing assessments
    existing_claim_ids = session.query(DamageAssessment.claim_id).distinct().all()
    existing_claim_ids = [c[0] for c in existing_claim_ids]

    high_risk_claims = session.query(Claim).join(FraudScore).filter(
        FraudScore.fraud_score >= 0.5,
        ~Claim.id.in_(existing_claim_ids)
    ).limit(len(image_files)).all()

    if not high_risk_claims:
        print("⚠️  No available high-risk claims to link to")
        print("Using any available claims instead...")

        high_risk_claims = session.query(Claim).filter(
            ~Claim.id.in_(existing_claim_ids)
        ).limit(len(image_files)).all()

    linked = 0

    for claim, img_path in zip(high_risk_claims, image_files):
        # Create damage assessment
        assessment = DamageAssessment(
            claim_id=claim.id,
            file_url=str(img_path.absolute()),
            file_type='image',
            damage_type=DamageType.DENT,
            severity=DamageSeverity.MODERATE,
            severity_score=50,
            affected_areas=[],
            estimated_cost_min=0,
            estimated_cost_max=0,
            ai_response='Pending AI analysis',
            model_version='pending',
            confidence_score=0.0,
            reviewed=False
        )

        session.add(assessment)
        print(f"✅ Linked {img_path.name} → Claim {claim.claim_number}")
        linked += 1

    session.commit()
    session.close()

    print("\n" + "="*60)
    print(f"✅ Successfully linked {linked} images to claims")
    print("\n📊 Next steps:")
    print("1. Open dashboard: http://localhost:7860")
    print("2. Go to 'Claim Details' tab")
    print("3. Search for linked claims to see images")
    print("4. Or upload images directly in 'Damage Assessment' tab")


if __name__ == "__main__":
    print("\n🛡️  ClaimGuard - Link Custom Images")
    print("="*60)
    link_custom_images()
