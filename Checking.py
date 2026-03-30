from pathlib import Path

# =========================
# CHANGE THIS IF NEEDED
# =========================
DATASET_PATH = Path("data")  # change if your dataset folder is somewhere else

SPLITS = ["Train", "Validation", "Test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
LABEL_EXTENSION = ".txt"


def get_files_by_stem(folder, valid_exts):
    files = {}
    if not folder.exists():
        return files

    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() in valid_exts:
            files[f.stem] = f.name
    return files


def check_split(split):
    print("\n" + "=" * 70)
    print(f"CHECKING SPLIT: {split}")

    images_dir = DATASET_PATH / split / "images"
    labels_dir = DATASET_PATH / split / "labels"

    if not images_dir.exists():
        print(f"[ERROR] Missing images folder: {images_dir}")
        return

    if not labels_dir.exists():
        print(f"[ERROR] Missing labels folder: {labels_dir}")
        return

    image_files = get_files_by_stem(images_dir, IMAGE_EXTENSIONS)
    label_files = get_files_by_stem(labels_dir, {LABEL_EXTENSION})

    image_stems = set(image_files.keys())
    label_stems = set(label_files.keys())

    missing_labels = sorted(image_stems - label_stems)
    missing_images = sorted(label_stems - image_stems)

    print(f"Total images: {len(image_stems)}")
    print(f"Total labels: {len(label_stems)}")
    print(f"Images without labels: {len(missing_labels)}")
    print(f"Labels without images: {len(missing_images)}")

    print("\n--- IMAGES WITHOUT LABELS ---")
    if missing_labels:
        for stem in missing_labels:
            print(image_files[stem])
    else:
        print("None")

    print("\n--- LABELS WITHOUT IMAGES ---")
    if missing_images:
        for stem in missing_images:
            print(label_files[stem])
    else:
        print("None")


# =========================
# RUN EVERYTHING
# =========================
print(f"Dataset path: {DATASET_PATH.resolve()}")

if not DATASET_PATH.exists():
    print(f"[ERROR] Dataset path does not exist: {DATASET_PATH}")
else:
    for split in SPLITS:
        check_split(split)