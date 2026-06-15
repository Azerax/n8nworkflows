import os, json, shutil
from pathlib import Path

ROOT = Path("workflows")
INDEX = Path("index.json")

items = []

dirs = sorted([p for p in ROOT.iterdir() if p.is_dir()], key=lambda p: p.name.lower())

for i, old_dir in enumerate(dirs, start=1):
    wid = f"{i:05d}"
    temp_dir = ROOT / f"__tmp_{wid}"
    final_dir = ROOT / wid

    original_name = old_dir.name
    temp_dir.mkdir()

    files = list(old_dir.iterdir())

    for file in files:
        if not file.is_file():
            continue

        suffix = file.suffix.lower()

        if suffix == ".json":
            if "metada" in file.name.lower() or "metadata" in file.name.lower():
                new_name = "metadata.json"
            else:
                new_name = "workflow.json"
        elif suffix == ".md":
            new_name = "readme.md"
        elif suffix == ".webp":
            new_name = "preview.webp"
        else:
            new_name = "asset" + suffix

        target = temp_dir / new_name

        count = 2
        while target.exists():
            stem = Path(new_name).stem
            ext = Path(new_name).suffix
            target = temp_dir / f"{stem}-{count}{ext}"
            count += 1

        shutil.move(str(file), str(target))

    shutil.rmtree(old_dir)

    items.append({
        "id": wid,
        "original_name": original_name,
        "path": f"workflows/{wid}",
        "files": sorted([p.name for p in temp_dir.iterdir()])
    })

for item in items:
    temp = ROOT / f"__tmp_{item['id']}"
    final = ROOT / item["id"]
    temp.rename(final)

INDEX.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Normalized {len(items)} workflow folders.")
print("Wrote index.json")
