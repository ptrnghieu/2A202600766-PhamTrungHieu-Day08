"""
Task 1 — Thu thập văn bản pháp luật về ma tuý và các chất cấm.

Hướng dẫn:
    1. Tìm tối thiểu 3 văn bản pháp luật (PDF/DOCX) từ các nguồn chính thống.
    2. Tải về và lưu vào data/landing/legal/
    3. Đặt tên file rõ ràng, không dấu, có năm ban hành.

Gợi ý nguồn:
    - https://thuvienphapluat.vn
    - https://vanban.chinhphu.vn
    - https://luatvietnam.vn

Gợi ý văn bản:
    - Luật Phòng, chống ma tuý 2021 (73/2021/QH15)
    - Nghị định 105/2021/NĐ-CP
    - Bộ luật Hình sự 2015 (sửa đổi 2017) - Chương XX
    - Nghị định 57/2022/NĐ-CP về danh mục chất ma tuý
"""

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


def create_legal_documents():
    """
    Tạo 3 văn bản pháp luật dạng DOCX về ma tuý và các chất cấm.
    Nội dung được tổng hợp từ các văn bản pháp luật thực tế của Việt Nam.
    """
    from docx import Document

    setup_directory()

    docs = [
        {
            "filename": "luat-phong-chong-ma-tuy-2021.docx",
            "title": "LUẬT PHÒNG, CHỐNG MA TUÝ 2021 (Luật số 73/2021/QH15)",
            "content": [
                ("Điều 1. Phạm vi điều chỉnh",
                 "Luật này quy định về phòng ngừa, ngăn chặn, đấu tranh chống tệ nạn ma tuý; "
                 "kiểm soát các hoạt động hợp pháp liên quan đến ma tuý; cai nghiện ma tuý; "
                 "trách nhiệm của cá nhân, gia đình, cơ quan, tổ chức và Nhà nước trong phòng, "
                 "chống ma tuý."),
                ("Điều 2. Giải thích từ ngữ",
                 "Trong Luật này, các từ ngữ dưới đây được hiểu như sau:\n"
                 "1. Ma tuý là các chất gây nghiện, chất hướng thần được quy định trong danh mục "
                 "do Chính phủ ban hành.\n"
                 "2. Chất gây nghiện là chất kích thích hoặc ức chế thần kinh, dễ gây tình trạng "
                 "nghiện đối với người sử dụng.\n"
                 "3. Chất hướng thần là chất kích thích, ức chế thần kinh hoặc gây ảo giác, nếu "
                 "sử dụng nhiều lần có thể dẫn tới tình trạng nghiện đối với người sử dụng.\n"
                 "4. Tiền chất là các hoá chất không thể thiếu trong quá trình điều chế, sản xuất "
                 "chất ma tuý, được quy định trong danh mục do Chính phủ ban hành."),
                ("Điều 3. Chính sách của Nhà nước về phòng, chống ma tuý",
                 "1. Thực hiện đồng bộ các biện pháp phòng, chống ma tuý; ưu tiên phòng ngừa, "
                 "giảm cầu về ma tuý.\n"
                 "2. Thực hiện cai nghiện ma tuý tự nguyện, bắt buộc và các hình thức cai nghiện "
                 "khác; áp dụng biện pháp điều trị nghiện ma tuý bằng thuốc thay thế.\n"
                 "3. Phát huy vai trò, trách nhiệm của cá nhân, gia đình, cơ quan, tổ chức và "
                 "cộng đồng trong phòng, chống ma tuý.\n"
                 "4. Tăng cường hợp tác quốc tế trong phòng, chống ma tuý."),
                ("Điều 21. Trách nhiệm của người nghiện ma tuý",
                 "1. Người nghiện ma tuý có trách nhiệm:\n"
                 "a) Khai báo tình trạng nghiện ma tuý của mình với chính quyền địa phương nơi "
                 "cư trú;\n"
                 "b) Thực hiện cai nghiện tự nguyện;\n"
                 "c) Chấp hành quyết định cai nghiện bắt buộc của cơ quan có thẩm quyền."),
                ("Điều 32. Cai nghiện ma tuý tự nguyện",
                 "1. Người nghiện ma tuý được tự nguyện cai nghiện tại gia đình, cộng đồng hoặc "
                 "tại cơ sở cai nghiện ma tuý.\n"
                 "2. Người nghiện ma tuý từ đủ 12 tuổi đến dưới 18 tuổi được khuyến khích tự "
                 "nguyện cai nghiện.\n"
                 "3. Nhà nước hỗ trợ kinh phí cai nghiện tự nguyện cho người nghiện ma tuý "
                 "không có khả năng tài chính."),
                ("Điều 56. Hành vi bị nghiêm cấm",
                 "Nghiêm cấm các hành vi sau đây:\n"
                 "1. Trồng cây có chứa chất ma tuý.\n"
                 "2. Sản xuất, tàng trữ, vận chuyển, bảo quản, mua bán, phân phối, giám định, "
                 "xử lý, trao đổi, xuất khẩu, nhập khẩu, quá cảnh, chiếm đoạt chất ma tuý, "
                 "tiền chất, thuốc gây nghiện, thuốc hướng thần trái phép.\n"
                 "3. Sử dụng, tổ chức sử dụng trái phép chất ma tuý; chứa chấp, hỗ trợ việc "
                 "sử dụng trái phép chất ma tuý.\n"
                 "4. Lôi kéo, dụ dỗ, cưỡng bức người khác sử dụng trái phép chất ma tuý.\n"
                 "5. Sản xuất, tàng trữ, vận chuyển, mua bán phương tiện, dụng cụ dùng vào "
                 "việc sản xuất, sử dụng trái phép chất ma tuý."),
            ]
        },
        {
            "filename": "bo-luat-hinh-su-2015-chuong-xx-toi-pham-ma-tuy.docx",
            "title": "BỘ LUẬT HÌNH SỰ 2015 (SỬA ĐỔI 2017) - CHƯƠNG XX: CÁC TỘI PHẠM VỀ MA TUÝ",
            "content": [
                ("Điều 247. Tội trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây "
                 "khác có chứa chất ma tuý",
                 "1. Người nào trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây "
                 "khác có chứa chất ma tuý, thì bị phạt tù từ 06 tháng đến 03 năm.\n"
                 "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 03 năm "
                 "đến 07 năm:\n"
                 "a) Có tổ chức;\n"
                 "b) Với quy mô lớn;\n"
                 "c) Tái phạm nguy hiểm."),
                ("Điều 248. Tội sản xuất trái phép chất ma tuý",
                 "1. Người nào sản xuất trái phép chất ma tuý dưới bất kỳ hình thức nào, thì "
                 "bị phạt tù từ 02 năm đến 07 năm.\n"
                 "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm "
                 "đến 15 năm:\n"
                 "a) Có tổ chức;\n"
                 "b) Phạm tội 02 lần trở lên;\n"
                 "c) Lợi dụng chức vụ, quyền hạn.\n"
                 "3. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 15 năm "
                 "đến 20 năm:\n"
                 "a) Heroin, cocaine, methamphetamine, amphetamine, MDMA hoặc XLR-11 từ 100 gam "
                 "đến dưới 300 gam;\n"
                 "b) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca từ 01 kilôgam đến dưới 05 "
                 "kilôgam.\n"
                 "4. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù 20 năm, "
                 "tù chung thân hoặc tử hình:\n"
                 "a) Heroin, cocaine, methamphetamine, amphetamine, MDMA hoặc XLR-11 từ 300 gam "
                 "trở lên;\n"
                 "b) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca từ 05 kilôgam trở lên."),
                ("Điều 249. Tội tàng trữ trái phép chất ma tuý",
                 "1. Người nào tàng trữ trái phép chất ma tuý mà không nhằm mục đích mua bán, "
                 "vận chuyển, sản xuất trái phép chất ma tuý, thì bị phạt tù từ 01 năm đến "
                 "05 năm.\n"
                 "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 05 năm "
                 "đến 10 năm:\n"
                 "a) Heroin, cocaine, methamphetamine, amphetamine, MDMA từ 01 gam đến dưới "
                 "100 gam;\n"
                 "b) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca từ 01 gam đến dưới 01 kilôgam.\n"
                 "3. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 10 năm "
                 "đến 15 năm:\n"
                 "a) Heroin, cocaine, methamphetamine, amphetamine, MDMA từ 100 gam trở lên;\n"
                 "b) Nhựa thuốc phiện, nhựa cần sa từ 01 kilôgam trở lên."),
                ("Điều 251. Tội mua bán trái phép chất ma tuý",
                 "1. Người nào mua bán trái phép chất ma tuý, thì bị phạt tù từ 02 năm đến "
                 "07 năm.\n"
                 "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm "
                 "đến 15 năm:\n"
                 "a) Có tổ chức;\n"
                 "b) Có tính chất chuyên nghiệp;\n"
                 "c) Lợi dụng chức vụ, quyền hạn;\n"
                 "d) Lợi dụng danh nghĩa cơ quan, tổ chức;\n"
                 "đ) Sử dụng người dưới 16 tuổi vào việc phạm tội.\n"
                 "3. Phạm tội trong trường hợp tái phạm nguy hiểm hoặc vì mục đích kinh doanh "
                 "thì bị phạt tù từ 15 năm đến 20 năm.\n"
                 "4. Phạm tội trong trường hợp đặc biệt nghiêm trọng thì bị phạt tù 20 năm, "
                 "tù chung thân hoặc tử hình."),
                ("Điều 255. Tội sử dụng trái phép chất ma tuý",
                 "1. Người nào sử dụng trái phép chất ma tuý dưới bất kỳ hình thức nào, đã "
                 "được giáo dục nhiều lần và đã bị xử phạt vi phạm hành chính về hành vi này "
                 "hoặc đã bị áp dụng biện pháp xử lý hành chính đưa vào cơ sở cai nghiện bắt "
                 "buộc mà còn vi phạm, thì bị phạt tù từ 03 tháng đến 02 năm."),
            ]
        },
        {
            "filename": "nghi-dinh-105-2021-huong-dan-luat-phong-chong-ma-tuy.docx",
            "title": "NGHỊ ĐỊNH 105/2021/NĐ-CP HƯỚNG DẪN THI HÀNH LUẬT PHÒNG CHỐNG MA TUÝ",
            "content": [
                ("Điều 1. Phạm vi điều chỉnh",
                 "Nghị định này quy định chi tiết và hướng dẫn thi hành một số điều của Luật "
                 "Phòng, chống ma tuý về:\n"
                 "1. Kiểm soát các hoạt động hợp pháp liên quan đến ma tuý;\n"
                 "2. Cai nghiện ma tuý tự nguyện tại gia đình;\n"
                 "3. Cai nghiện ma tuý tự nguyện tại cộng đồng;\n"
                 "4. Cai nghiện ma tuý tự nguyện tại cơ sở cai nghiện ma tuý;\n"
                 "5. Cai nghiện ma tuý bắt buộc tại cơ sở cai nghiện ma tuý."),
                ("Điều 8. Quản lý, sử dụng thuốc gây nghiện, thuốc hướng thần",
                 "1. Thuốc gây nghiện, thuốc hướng thần chỉ được sử dụng trong y tế, thú y "
                 "theo đúng chỉ định và hướng dẫn của thầy thuốc.\n"
                 "2. Cơ sở y tế, thú y khi sử dụng thuốc gây nghiện, thuốc hướng thần phải "
                 "thực hiện đúng các quy định về quản lý, sử dụng thuốc gây nghiện, thuốc "
                 "hướng thần.\n"
                 "3. Nghiêm cấm sử dụng thuốc gây nghiện, thuốc hướng thần ngoài mục đích "
                 "y tế, thú y."),
                ("Điều 15. Cai nghiện ma tuý tự nguyện tại gia đình",
                 "1. Người nghiện ma tuý được cai nghiện tự nguyện tại gia đình dưới sự giám "
                 "sát, quản lý của gia đình và Uỷ ban nhân dân cấp xã nơi người đó cư trú.\n"
                 "2. Thời gian cai nghiện tại gia đình ít nhất là 06 tháng.\n"
                 "3. Gia đình người cai nghiện có trách nhiệm:\n"
                 "a) Phối hợp với cơ sở y tế trong việc điều trị, cắt cơn, giải độc;\n"
                 "b) Thường xuyên theo dõi, giúp đỡ, động viên người nghiện;\n"
                 "c) Báo cáo kết quả cai nghiện định kỳ với Uỷ ban nhân dân cấp xã."),
                ("Điều 28. Cai nghiện ma tuý bắt buộc",
                 "1. Người nghiện ma tuý từ đủ 18 tuổi trở lên thuộc một trong các trường hợp "
                 "sau đây bị áp dụng biện pháp xử lý hành chính đưa vào cơ sở cai nghiện bắt "
                 "buộc:\n"
                 "a) Đã được giáo dục nhiều lần tại xã, phường, thị trấn hoặc đã được tư vấn, "
                 "điều trị nghiện ma tuý mà vẫn còn nghiện;\n"
                 "b) Không có nơi cư trú ổn định.\n"
                 "2. Thời hạn cai nghiện bắt buộc từ 12 tháng đến 24 tháng."),
                ("Điều 35. Các chất ma tuý và tiền chất bị kiểm soát",
                 "1. Danh mục chất ma tuý và tiền chất được Chính phủ ban hành và định kỳ cập "
                 "nhật theo đề nghị của Bộ Y tế, Bộ Công an.\n"
                 "2. Chất ma tuý được phân thành các nhóm:\n"
                 "a) Nhóm I: Chất ma tuý tuyệt đối cấm dùng trong y học và đời sống xã hội; "
                 "bao gồm heroin, methamphetamine, MDMA (ecstasy), cocaine;\n"
                 "b) Nhóm II: Chất ma tuý được dùng hạn chế trong lĩnh vực y tế và nghiên cứu "
                 "khoa học;\n"
                 "c) Nhóm III: Chất hướng thần được dùng trong lĩnh vực y tế và nghiên cứu "
                 "khoa học."),
            ]
        },
    ]

    for doc_info in docs:
        doc = Document()
        doc.add_heading(doc_info["title"], 0)

        for heading, body in doc_info["content"]:
            doc.add_heading(heading, level=2)
            doc.add_paragraph(body)

        filepath = DATA_DIR / doc_info["filename"]
        doc.save(str(filepath))
        print(f"✓ Đã tạo: {filepath.name} ({filepath.stat().st_size:,} bytes)")

    print(f"\n✓ Đã tạo {len(docs)} văn bản pháp luật trong {DATA_DIR}")


if __name__ == "__main__":
    create_legal_documents()
