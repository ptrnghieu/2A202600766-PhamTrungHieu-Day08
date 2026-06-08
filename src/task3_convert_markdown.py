"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft:
    https://github.com/microsoft/markitdown

Cài đặt:
    pip install markitdown

Hướng dẫn:
    1. Scan toàn bộ file trong data/landing/ (PDF, DOCX, DOC, JSON)
    2. Convert sang Markdown
    3. Lưu vào data/standardized/ giữ nguyên cấu trúc thư mục

Xử lý các định dạng:
    - .docx  → MarkItDown
    - .pdf   → pdftotext (có text layer) hoặc Tesseract OCR (scanned PDF)
    - .doc   → wvText (wv package)
    - .json  → extract content_markdown field
"""

import json
import subprocess
from pathlib import Path

from markitdown import MarkItDown

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def _pdf_to_text(filepath: Path) -> str:
    """
    Trích xuất text từ PDF.
    - Dùng pdftotext nếu PDF có text layer.
    - Fallback sang Tesseract OCR nếu PDF là scan.
    """
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(filepath), "-"],
            capture_output=True, text=True, timeout=60
        )
        text = result.stdout.strip()
        # Nếu nội dung quá ít (< 200 chars) → PDF scanned → dùng OCR
        if len(text) < 200:
            print(f"    → PDF scanned, chuyển sang OCR (có thể mất vài phút)...")
            text = _ocr_pdf(filepath)
    except FileNotFoundError:
        print("    ⚠ pdftotext không có. Thử OCR...")
        text = _ocr_pdf(filepath)
    return text


def _ocr_pdf(filepath: Path) -> str:
    """OCR từng trang PDF bằng Tesseract (Vietnamese)."""
    import tempfile
    import os

    pages_text = []
    # Chuyển PDF → ảnh từng trang
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["pdftoppm", "-r", "150", str(filepath), f"{tmpdir}/page"],
            capture_output=True, timeout=300
        )
        if result.returncode != 0:
            return ""

        page_images = sorted(Path(tmpdir).glob("page-*.ppm"))
        total = len(page_images)
        print(f"    → OCR {total} trang...")

        for i, img_path in enumerate(page_images, 1):
            if i % 10 == 0:
                print(f"      Đang xử lý trang {i}/{total}...")
            ocr_result = subprocess.run(
                ["tesseract", str(img_path), "stdout", "-l", "vie", "--psm", "1"],
                capture_output=True, text=True, timeout=60
            )
            if ocr_result.returncode == 0:
                pages_text.append(ocr_result.stdout)

    return "\n\n".join(pages_text)


def _doc_to_text(filepath: Path) -> str:
    """Trích xuất text từ .doc (định dạng cũ) bằng wvText."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["wvText", str(filepath), tmp_path],
            capture_output=True, text=True, timeout=30
        )
        text = Path(tmp_path).read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        # wv không có, thử MarkItDown
        try:
            md = MarkItDown()
            result = md.convert(str(filepath))
            text = result.text_content
        except Exception:
            text = ""
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return text


def convert_legal_docs():
    """Convert PDF/DOCX/DOC files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    md_converter = MarkItDown()

    converted = 0
    for filepath in sorted(legal_dir.iterdir()):
        suffix = filepath.suffix.lower()
        if suffix not in (".pdf", ".docx", ".doc"):
            continue

        print(f"Converting: {filepath.name}")
        try:
            if suffix == ".docx":
                result = md_converter.convert(str(filepath))
                text = result.text_content
            elif suffix == ".pdf":
                text = _pdf_to_text(filepath)
            elif suffix == ".doc":
                text = _doc_to_text(filepath)
            else:
                continue

            if not text.strip():
                print(f"  ✗ Không trích xuất được nội dung từ {filepath.name}")
                continue

            output_path = output_dir / f"{filepath.stem}.md"
            output_path.write_text(text, encoding="utf-8")
            print(f"  ✓ Saved: {output_path.name} ({len(text):,} chars)")
            converted += 1
        except Exception as e:
            print(f"  ✗ Failed: {filepath.name} — {e}")

    return converted


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    for filepath in sorted(news_dir.iterdir()):
        if filepath.suffix.lower() == ".json":
            print(f"Converting: {filepath.name}")
            try:
                data = json.loads(filepath.read_text(encoding="utf-8"))
                output_path = output_dir / f"{filepath.stem}.md"

                # Build markdown with metadata header
                header = f"# {data.get('title', 'Unknown')}\n\n"
                header += f"**Source:** {data.get('url', 'N/A')}\n"
                header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n\n---\n\n"

                content = header + data.get("content_markdown", "")
                output_path.write_text(content, encoding="utf-8")
                print(f"  ✓ Saved: {output_path.name} ({len(content):,} chars)")
                converted += 1
            except Exception as e:
                print(f"  ✗ Failed: {filepath.name} — {e}")

    return converted


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    legal_count = convert_legal_docs()

    print("\n--- News Articles ---")
    news_count = convert_news_articles()

    print(f"\n✓ Done! Converted {legal_count} legal + {news_count} news files")
    print(f"  Output tại: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
