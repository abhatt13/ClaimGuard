"""
Train YOLOv5 custom model for vehicle damage detection
"""

import sys
import os
from pathlib import Path
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def check_dataset():
    """Check if Roboflow dataset is available"""

    dataset_path = Path("data/raw/roboflow_yolo")

    if not dataset_path.exists():
        print("❌ Dataset not found!")
        print("\nPlease download the dataset first:")
        print("1. See instructions in: ROBOFLOW_SETUP.md")
        print("2. Or run: python scripts/download_roboflow_yolo.py")
        return False

    # Check for data.yaml
    yaml_file = dataset_path / "data.yaml"
    if not yaml_file.exists():
        print(f"❌ data.yaml not found in {dataset_path}")
        return False

    # Check for images
    train_path = dataset_path / "train" / "images"
    if not train_path.exists() or not list(train_path.glob("*.jpg")):
        print(f"❌ No training images found in {train_path}")
        return False

    print("✅ Dataset found and valid!")
    return True


def setup_yolov5():
    """Clone and set up YOLOv5"""

    yolo_path = Path("models/yolov5")

    if yolo_path.exists():
        print("✅ YOLOv5 already cloned")
        return yolo_path

    print("📥 Cloning YOLOv5 repository...")

    import subprocess

    try:
        subprocess.run(
            ["git", "clone", "https://github.com/ultralytics/yolov5.git", str(yolo_path)],
            check=True,
            capture_output=True
        )
        print("✅ YOLOv5 cloned successfully")

        # Install requirements
        print("📦 Installing YOLOv5 dependencies...")
        subprocess.run(
            ["pip", "install", "-r", str(yolo_path / "requirements.txt"), "--quiet"],
            check=True
        )
        print("✅ Dependencies installed")

        return yolo_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up YOLOv5: {e}")
        return None


def train_model(model_size="s", epochs=50, batch_size=16, img_size=640):
    """
    Train YOLOv5 model on car damage dataset

    Args:
        model_size: Model size (n, s, m, l, x) - 's' recommended for balance
        epochs: Number of training epochs
        batch_size: Batch size (reduce if running out of memory)
        img_size: Image size for training
    """

    print("\n" + "="*60)
    print("🚀 Training YOLOv5 Custom Damage Detection Model")
    print("="*60 + "\n")

    # Check dataset
    if not check_dataset():
        return

    # Setup YOLOv5
    yolo_path = setup_yolov5()
    if not yolo_path:
        return

    # Training configuration
    data_yaml = Path("data/raw/roboflow_yolo/data.yaml").absolute()
    weights = f"yolov5{model_size}.pt"

    print(f"\n📊 Training Configuration:")
    print(f"  - Model: YOLOv5{model_size}")
    print(f"  - Epochs: {epochs}")
    print(f"  - Batch size: {batch_size}")
    print(f"  - Image size: {img_size}")
    print(f"  - Dataset: {data_yaml}")
    print(f"  - Device: {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'}")

    # Estimate training time
    device_type = "GPU" if torch.cuda.is_available() else "CPU"
    time_estimate = {
        "GPU": "~30-60 minutes",
        "CPU": "~2-4 hours"
    }
    print(f"\n⏱️  Estimated training time: {time_estimate[device_type]}")

    print("\n" + "="*60)
    input("Press Enter to start training (or Ctrl+C to cancel)...")
    print("="*60 + "\n")

    # Change to YOLOv5 directory
    os.chdir(yolo_path)

    # Train command
    train_script = yolo_path / "train.py"

    import subprocess

    cmd = [
        "python", str(train_script),
        "--img", str(img_size),
        "--batch", str(batch_size),
        "--epochs", str(epochs),
        "--data", str(data_yaml),
        "--weights", weights,
        "--project", "../../app/ml/models/yolo_damage",
        "--name", "damage_detector_v1",
        "--cache"
    ]

    print("🏋️  Training started...\n")

    try:
        result = subprocess.run(cmd, check=True)

        print("\n" + "="*60)
        print("✅ Training Complete!")
        print("="*60)

        # Show results location
        results_path = Path("../../app/ml/models/yolo_damage/damage_detector_v1")
        print(f"\n📁 Results saved to: {results_path}")
        print(f"\n🎯 Best model: {results_path / 'weights' / 'best.pt'}")

        print("\n📊 View training results:")
        print(f"  - Metrics: {results_path / 'results.png'}")
        print(f"  - Predictions: {results_path / 'val_batch0_pred.jpg'}")

        print("\n🚀 Next steps:")
        print("1. Test model: python scripts/test_yolo_model.py")
        print("2. Integrate into ClaimGuard dashboard")
        print("3. Compare with OpenAI Vision API")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed: {e}")
        print("\nTry reducing batch size if running out of memory:")
        print("  python scripts/train_yolo_damage.py --batch-size 8")

    finally:
        # Return to project root
        os.chdir("../..")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train YOLOv5 damage detection model")
    parser.add_argument("--model", default="s", choices=["n", "s", "m", "l", "x"],
                       help="Model size (n=nano, s=small, m=medium, l=large, x=xlarge)")
    parser.add_argument("--epochs", type=int, default=50,
                       help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=16,
                       help="Batch size for training")
    parser.add_argument("--img-size", type=int, default=640,
                       help="Image size for training")

    args = parser.parse_args()

    train_model(
        model_size=args.model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        img_size=args.img_size
    )
