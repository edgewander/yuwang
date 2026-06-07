#!/usr/bin/env python3
"""
批量将 docs/images/ 下的 jpg/jpeg/png 转换为 webp（多进程并行版）
"""
import os
import re
from pathlib import Path
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

PROJECT_ROOT = Path("C:/Users/wshen/Documents/prison-art/yuwang")
IMAGES_DIR = PROJECT_ROOT / "docs" / "images"
DOCS_DIR = PROJECT_ROOT / "docs"

stats = {
    "converted": 0,
    "skipped_existing": 0,
    "skipped_webp": 0,
    "skipped_gif": 0,
    "errors": 0,
    "original_size": 0,
    "webp_size": 0,
}


def convert_single(args):
    """转换单个文件，返回结果字典。"""
    img_path, idx, total = args
    ext = img_path.suffix.lower()

    # 检查是否已有对应的 webp
    webp_path = img_path.with_suffix(".webp")
    if webp_path.exists():
        return {"type": "skipped_existing", "path": str(img_path)}

    if ext == ".webp":
        return {"type": "skipped_webp", "path": str(img_path)}
    if ext == ".gif":
        return {"type": "skipped_gif", "path": str(img_path)}
    if ext not in (".jpg", ".jpeg", ".png"):
        return {"type": "skipped_other", "path": str(img_path)}

    try:
        original_size = img_path.stat().st_size
        img = Image.open(img_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        img.save(webp_path, "WEBP", quality=85, method=6)
        webp_size = webp_path.stat().st_size

        # 删除原图
        img_path.unlink()

        return {
            "type": "converted",
            "path": str(img_path),
            "original_size": original_size,
            "webp_size": webp_size,
        }
    except Exception as e:
        if webp_path.exists():
            webp_path.unlink()
        return {"type": "error", "path": str(img_path), "error": str(e)}


def update_markdown_references():
    """更新所有 markdown 文件中的图片引用后缀。"""
    md_files = list(DOCS_DIR.glob("*.md"))
    print(f"\n扫描 {len(md_files)} 个 markdown 文件...")

    replacements = [
        (".jpg", ".webp"),
        (".jpeg", ".webp"),
        (".png", ".webp"),
        (".JPG", ".webp"),
        (".JPEG", ".webp"),
        (".PNG", ".webp"),
        (".JpG", ".webp"),
    ]

    updated_files = 0
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        original = content

        for old_ext, new_ext in replacements:
            pattern = re.escape(old_ext) + r'(?=\))'
            content = re.sub(pattern, new_ext, content)

        if content != original:
            md_file.write_text(content, encoding="utf-8")
            updated_files += 1

    print(f"更新了 {updated_files} 个 markdown 文件")


def main():
    print("=" * 60)
    print("监狱博物馆图片批量 WebP 转换（多进程并行版）")
    print("=" * 60)

    image_files = [f for f in IMAGES_DIR.iterdir() if f.is_file()]
    print(f"发现 {len(image_files)} 个图片文件\n")

    workers = min(multiprocessing.cpu_count(), 8)
    print(f"使用 {workers} 个并行进程\n")

    # 准备任务列表
    tasks = [(f, i, len(image_files)) for i, f in enumerate(image_files, 1)]

    converted_count = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(convert_single, t): t for t in tasks}
        for future in as_completed(futures):
            result = future.result()
            rtype = result["type"]

            if rtype == "converted":
                stats["converted"] += 1
                stats["original_size"] += result["original_size"]
                stats["webp_size"] += result["webp_size"]
                converted_count += 1
                if converted_count % 200 == 0:
                    print(f"  进度: {converted_count} 已转换...")
            elif rtype == "skipped_existing":
                stats["skipped_existing"] += 1
            elif rtype == "skipped_webp":
                stats["skipped_webp"] += 1
            elif rtype == "skipped_gif":
                stats["skipped_gif"] += 1
            elif rtype == "error":
                stats["errors"] += 1
                print(f"[ERROR] {result['path']}: {result['error']}")

    print(f"\n转换完成:")
    print(f"  新转换: {stats['converted']}")
    print(f"  已存在(webp): {stats['skipped_existing']}")
    print(f"  跳过(WebP): {stats['skipped_webp']}")
    print(f"  跳过(GIF): {stats['skipped_gif']}")
    print(f"  错误: {stats['errors']}")

    # 更新 markdown
    print("\n更新 Markdown 引用...")
    update_markdown_references()

    # 统计
    print("\n" + "=" * 60)
    print("体积对比")
    print("=" * 60)
    original_mb = stats["original_size"] / 1024 / 1024
    webp_mb = stats["webp_size"] / 1024 / 1024
    saved_mb = original_mb - webp_mb
    ratio = (saved_mb / original_mb * 100) if original_mb > 0 else 0

    print(f"  原始体积: {original_mb:.1f} MB")
    print(f"  WebP 体积: {webp_mb:.1f} MB")
    print(f"  节省: {saved_mb:.1f} MB ({ratio:.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    main()
