"""
Download datasets for ClaimGuard.
This script helps you get the Kaggle fraud dataset and VehiDE images.
"""

import os
import subprocess
import sys
from pathlib import Path

# Color codes for terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_step(step, message):
    print(f"\n{BLUE}[Step {step}]{RESET} {message}")


def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")


def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")


def print_error(message):
    print(f"{RED}❌ {message}{RESET}")


def check_kaggle_setup():
    """Check if Kaggle is configured"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'

    if kaggle_json.exists():
        print_success("Kaggle API credentials found")
        return True
    else:
        print_warning("Kaggle API not configured")
        return False


def setup_kaggle():
    """Guide user through Kaggle setup"""
    print("\n" + "="*60)
    print("📋 Kaggle API Setup Instructions")
    print("="*60)

    print("""
1. Go to: https://www.kaggle.com/
2. Sign in or create account (it's FREE)
3. Go to: https://www.kaggle.com/settings/account
4. Scroll to "API" section
5. Click "Create New Token"
6. This downloads kaggle.json

7. Move kaggle.json to the right location:
""")

    if sys.platform == "win32":
        print("   Windows: C:\\Users\\YourUsername\\.kaggle\\kaggle.json")
    else:
        print("   Mac/Linux: ~/.kaggle/kaggle.json")

    print("\n8. Run this script again after setup")

    input("\nPress Enter when you've completed these steps...")


def download_kaggle_fraud_data():
    """Download insurance fraud dataset from Kaggle"""
    print_step(1, "Downloading Kaggle Insurance Fraud Dataset")

    # Check if kaggle is installed
    try:
        import kaggle
        print_success("Kaggle package installed")
    except ImportError:
        print_warning("Installing kaggle package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        import kaggle

    # Check API setup
    if not check_kaggle_setup():
        setup_kaggle()
        return False

    # Create directory
    data_dir = Path("data/raw/kaggle_fraud")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Download dataset
    print("Downloading dataset (this may take a few minutes)...")

    try:
        # Dataset: Insurance Fraud Detection
        os.system(f"kaggle datasets download -d buntyshah/insurance-claims-fraud-detection -p {data_dir} --unzip")
        print_success(f"Dataset downloaded to: {data_dir}")

        # List downloaded files
        files = list(data_dir.glob("*.csv"))
        if files:
            print(f"\nDownloaded files:")
            for f in files:
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  - {f.name} ({size_mb:.2f} MB)")

        return True
    except Exception as e:
        print_error(f"Download failed: {e}")
        print("\nTry these alternatives:")
        print("1. https://www.kaggle.com/datasets/buntyshah/insurance-claims-fraud-detection")
        print("2. https://www.kaggle.com/datasets/mastmustu/insurance-claims-fraud-data")
        return False


def download_vehide_images():
    """Guide for downloading VehiDE vehicle damage images"""
    print_step(2, "VehiDE Vehicle Damage Image Dataset")

    print("""
The VehiDE dataset contains 13,945 vehicle damage images.

⚠️  This is a large dataset (several GB). For development, you can:

Option A: Download Sample (Recommended for testing)
  We'll use a smaller public dataset instead:
  - Roboflow Car Damage: 300+ images (FREE)
  - Good enough for testing AI vision

Option B: Full VehiDE Dataset
  - Research paper: https://www.tandfonline.com/doi/full/10.1080/24751839.2024.2367387
  - May require academic access or email authors
  - Download size: ~5-10 GB

For now, let's use the Roboflow dataset (easier access).
""")

    choice = input("\nDownload Roboflow sample dataset? (y/n): ").lower()

    if choice == 'y':
        print("\n📥 Downloading Roboflow Car Damage Dataset...")
        print("\nManual steps:")
        print("1. Go to: https://universe.roboflow.com/car-damage-kadad/car-damage-images")
        print("2. Click 'Download Dataset'")
        print("3. Select format: 'Folder Structure'")
        print("4. Download and extract to: data/raw/roboflow_damage/")
        print("\nOr use Roboflow CLI:")
        print("  pip install roboflow")
        print('  python -c "from roboflow import Roboflow; rf = Roboflow(api_key=\'YOUR_KEY\'); project = rf.workspace(\'car-damage-kadad\').project(\'car-damage-images\'); dataset = project.version(1).download(\'folder\')"')

        data_dir = Path("data/raw/roboflow_damage")
        data_dir.mkdir(parents=True, exist_ok=True)
        print_success(f"Directory created: {data_dir}")

    return True


def download_sample_policy_pdfs():
    """Create sample policy documents for RAG testing"""
    print_step(3, "Creating Sample Policy Documents")

    policy_dir = Path("data/policies")
    policy_dir.mkdir(parents=True, exist_ok=True)

    # Create a sample policy text file
    sample_policy = """
AUTOMOBILE INSURANCE POLICY

Policy Number: POL-2024-001
Policyholder: John Doe
Effective Date: January 1, 2024
Expiration Date: January 1, 2025

COVERAGE DETAILS:

1. COLLISION COVERAGE
   - Covers damage to your vehicle from collision with another vehicle or object
   - Coverage Limit: $50,000
   - Deductible: $500

2. COMPREHENSIVE COVERAGE
   - Covers damage from theft, vandalism, weather, fire
   - Coverage Limit: $50,000
   - Deductible: $250

3. LIABILITY COVERAGE
   - Bodily Injury: $100,000 per person / $300,000 per accident
   - Property Damage: $50,000 per accident

EXCLUSIONS:
- Intentional damage
- Racing or competitive events
- Damage while under influence of alcohol/drugs
- Wear and tear, mechanical breakdown
- Damage to custom equipment not declared

CLAIMS PROCESS:
1. Report incident within 24 hours
2. File police report if applicable
3. Submit photos of damage
4. Obtain repair estimates
5. Claim reviewed within 3 business days
"""

    sample_file = policy_dir / "sample_auto_policy.txt"
    sample_file.write_text(sample_policy)

    print_success(f"Sample policy created: {sample_file}")
    print("  You can add real policy PDFs to this directory later")

    return True


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║              🛡️  ClaimGuard Dataset Downloader            ║
║                                                           ║
║  This script will help you download the datasets needed  ║
║  for training and testing the AI models                  ║
╚═══════════════════════════════════════════════════════════╝
""")

    # Download Kaggle fraud data
    success_kaggle = download_kaggle_fraud_data()

    # Download vehicle damage images
    download_vehide_images()

    # Create sample policies
    download_sample_policy_pdfs()

    print("\n" + "="*60)
    print("📊 Dataset Download Summary")
    print("="*60)

    if success_kaggle:
        print_success("Kaggle fraud data: Ready")
    else:
        print_warning("Kaggle fraud data: Manual download needed")

    print_warning("Vehicle damage images: Manual download needed")
    print_success("Sample policy documents: Created")

    print("""
\n📋 Next Steps:
1. Complete any manual downloads above
2. Create .env file with API keys
3. Run: docker-compose up -d
4. Run: alembic upgrade head
5. Run: python scripts/ingest_data.py

Cost estimate with sample data:
  - 1,000 claims with images: ~$15-20 for OpenAI API
  - Stay well under $50/month budget ✅
""")


if __name__ == "__main__":
    main()
