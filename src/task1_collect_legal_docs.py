"""
Task 1 — Thu thập văn bản pháp luật về ma tuý và các chất cấm.

Nguồn văn bản thực tế (tải từ cổng thông tin chính thức):
    - Luật 73/2021/QH14: Luật Phòng, chống ma túy (30/3/2021)
      Nguồn: Công Báo số 567+568/Ngày 30-4-2021 (vanban.chinhphu.vn)
    - NĐ 105/2021/NĐ-CP: Quy định chi tiết một số điều Luật PCMT (4/12/2021)
      Nguồn: Cổng Thông tin điện tử Chính phủ (chinhphu.vn)
    - Cac_toi_pham_ve_ma_tuy_theo_quy_dinh_cua_BLHS.doc: Tổng hợp các tội
      phạm về ma tuý theo BLHS 2015 (sửa đổi 2017), Chương XX Điều 247-259
      Nguồn: Cơ quan Cảnh sát điều tra / tài liệu nghiệp vụ
"""

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

# Tên file chuẩn sau khi đã copy vào repo
LEGAL_FILES = [
    "luat-phong-chong-ma-tuy-73-2021-QH14.pdf",
    "nghi-dinh-105-2021-ND-CP.pdf",
    "cac-toi-pham-ve-ma-tuy-BLHS-2015.doc",
]


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


def create_legal_documents():
    """
    Kiểm tra và liệt kê 3 văn bản pháp luật THỰC ĐÃ được thu thập.

    Các file này là văn bản gốc (PDF/DOC) tải trực tiếp từ cổng thông tin
    điện tử của Chính phủ và Công Báo — không phải tài liệu tổng hợp.
    """
    setup_directory()

    found = []
    for fname in LEGAL_FILES:
        fpath = DATA_DIR / fname
        if fpath.exists():
            size = fpath.stat().st_size
            print(f"✓ Có sẵn: {fname} ({size:,} bytes)")
            found.append(fpath)
        else:
            print(f"✗ Thiếu: {fname} — cần copy file vào {DATA_DIR}")

    if len(found) == len(LEGAL_FILES):
        print(f"\n✓ Đủ {len(LEGAL_FILES)} văn bản pháp luật trong {DATA_DIR}")
    else:
        print(f"\n⚠ Chỉ có {len(found)}/{len(LEGAL_FILES)} file. Thiếu {len(LEGAL_FILES) - len(found)} file.")

    return found


if __name__ == "__main__":
    create_legal_documents()
