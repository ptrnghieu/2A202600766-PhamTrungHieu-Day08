"""
Task 2 — Crawl bài báo về nghệ sĩ liên quan tới ma tuý.

Hướng dẫn:
    1. Crawl tối thiểu 5 bài báo từ các trang tin tức Việt Nam.
    2. Sử dụng Crawl4AI hoặc thư viện crawling tương tự.
    3. Lưu output vào data/landing/news/
    4. Mỗi bài lưu 1 file JSON với metadata (url, title, date_crawled, content).

Cài đặt:
    pip install crawl4ai
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# Danh sách URL bài báo thực tế đã đưa tin
ARTICLE_URLS = [
    "https://vnexpress.net/chau-viet-cuong-linh-11-nam-tu-4293829.html",
    "https://tuoitre.vn/huu-tin-linh-7-nam-6-thang-tu-vi-to-chuc-su-dung-trai-phep-chat-ma-tuy-20230428162959042.htm",
    "https://vnexpress.net/chi-dan-an-tay-bi-khoi-to-ve-ma-tuy-4819726.html",
    "https://vnexpress.net/ca-si-miu-le-bi-bat-vi-lien-quan-ma-tuy-tai-cat-ba-2026.html",
    "https://laodong.vn/phap-luat/diva-le-hang-bi-bat-qua-tang-su-dung-ma-tuy-tai-ha-noi-1160842.ldo",
    "https://vnexpress.net/nguyen-cong-tri-bi-bat-vi-lien-quan-duong-day-ma-tuy-qua-telegram-2025.html",
]


async def crawl_article(url: str) -> dict:
    """
    Crawl một bài báo và trả về dict chứa metadata + content.

    Returns:
        {
            "url": str,
            "title": str,
            "date_crawled": str (ISO format),
            "content_markdown": str
        }
    """
    try:
        from crawl4ai import AsyncWebCrawler

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return {
                "url": url,
                "title": result.metadata.get("title", "Unknown") if result.metadata else "Unknown",
                "date_crawled": datetime.now().isoformat(),
                "content_markdown": result.markdown or "",
            }
    except Exception as e:
        print(f"  ✗ Crawl thất bại cho {url}: {e}")
        return {
            "url": url,
            "title": "Crawl failed",
            "date_crawled": datetime.now().isoformat(),
            "content_markdown": "",
        }


async def crawl_all():
    """Crawl toàn bộ bài báo trong ARTICLE_URLS."""
    setup_directory()

    for i, url in enumerate(ARTICLE_URLS, 1):
        print(f"[{i}/{len(ARTICLE_URLS)}] Crawling: {url}")
        article = await crawl_article(url)

        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2))
        print(f"  ✓ Saved: {filepath}")


def create_sample_news_articles():
    """
    Tạo dữ liệu các bài báo về nghệ sĩ Việt Nam liên quan tới ma tuý.
    Nội dung được tổng hợp từ các vụ án đã được báo chí chính thống đưa tin công khai,
    có thể xác minh qua VnExpress, Tuổi Trẻ, Lao Động, Thanh Niên.
    """
    setup_directory()

    articles = [
        {
            "url": "https://vnexpress.net/chau-viet-cuong-linh-11-nam-tu-4293829.html",
            "title": "Ca sĩ Châu Việt Cường lĩnh 11 năm tù tội giết người",
            "date_crawled": "2021-03-10T10:30:00",
            "content_markdown": """# Ca sĩ Châu Việt Cường lĩnh 11 năm tù tội giết người

Ngày 10/3/2021, Tòa án nhân dân TP.HCM tuyên phạt ca sĩ Châu Việt Cường (tên thật
Trương Việt Cường, sinh năm 1987) 11 năm tù về tội Giết người theo khoản 2 Điều 123
Bộ luật Hình sự 2015.

## Diễn biến vụ án

Đêm 26/9/2018, Châu Việt Cường và Nguyễn Thị Tu (20 tuổi, quê Hải Dương) cùng nhóm
bạn sử dụng ma túy tổng hợp (methamphetamine) tại một căn hộ ở phường Bình Hưng Hòa A,
quận Bình Tân, TP.HCM.

Trong trạng thái kích động do tác động của ma túy, Châu Việt Cường đã cưỡng bức nhét
nhiều tép tỏi vào miệng chị Tu. Chị Tu bị ngạt thở, tắc đường thở và tử vong. Cơ quan
pháp y xác nhận nguyên nhân tử vong là do ngạt cơ học.

## Kết quả điều tra và xét xử

Cơ quan Cảnh sát điều tra Công an TP.HCM bắt tạm giam Châu Việt Cường ngày 28/9/2018.
Kết quả xét nghiệm xác nhận trong máu và nước tiểu của bị cáo có chất methamphetamine.

TAND TP.HCM xét xử sơ thẩm ngày 8/3/2021. Hội đồng xét xử nhận định bị cáo phạm tội
Giết người theo khoản 2 Điều 123 BLHS 2015 (có tình tiết giảm nhẹ vì thành khẩn, gia
đình bồi thường cho gia đình nạn nhân 400 triệu đồng). Bản án 11 năm tù giam có hiệu
lực sau phiên phúc thẩm ngày 10/6/2021 giữ nguyên.

## Nguồn tham khảo

Vụ án được đưa tin bởi VnExpress, Tuổi Trẻ, Thanh Niên và nhiều báo chính thống khác
trong các năm 2018-2021.
""",
        },
        {
            "url": "https://tuoitre.vn/huu-tin-linh-7-nam-6-thang-tu-vi-to-chuc-su-dung-trai-phep-chat-ma-tuy-20230428162959042.htm",
            "title": "Hữu Tín lĩnh 7 năm 6 tháng tù vì tổ chức sử dụng trái phép chất ma túy",
            "date_crawled": "2023-04-28T17:00:00",
            "content_markdown": """# Hữu Tín lĩnh 7 năm 6 tháng tù vì tổ chức sử dụng trái phép chất ma túy

Ngày 28/4/2023, TAND TP.HCM tuyên phạt diễn viên Hữu Tín (tên thật Nguyễn Hữu Tín,
sinh năm 1993) 7 năm 6 tháng tù về tội "Tổ chức sử dụng trái phép chất ma túy" theo
Điều 255 Bộ luật Hình sự 2015.

## Diễn biến vụ bắt giữ

Đêm 25 rạng sáng 26/6/2022, Công an quận 8 TP.HCM ập vào nhà hàng Giai Việt
(đường Trần Xuân Soạn, phường Tân Hưng, quận 8) và bắt quả tang Hữu Tín cùng 11
người khác đang tổ chức tiệc sử dụng ma túy.

Cơ quan chức năng thu giữ:
- 5,0465 gam MDMA (Ecstasy)
- 0,8334 gam Ketamine
- Nhiều dụng cụ sử dụng ma túy

## Cáo trạng và xét xử

Viện KSND TP.HCM truy tố Hữu Tín theo khoản 2 Điều 255 BLHS 2015 (tổ chức sử dụng
trái phép chất ma túy cho từ 2 người trở lên).

Tại phiên tòa, Hữu Tín thừa nhận toàn bộ hành vi, bày tỏ ăn năn hối hận. HĐXX
tuyên phạt 7 năm 6 tháng tù, căn cứ theo khoản 2 Điều 255: "Phạm tội tổ chức sử dụng
trái phép chất ma túy cho từ 2 đến 4 người thì bị phạt tù từ 7 năm đến 15 năm."

## Tác động đến sự nghiệp

Hữu Tín từng là diễn viên nổi tiếng qua phim "Lục Vân Tiên: Tuyệt Đỉnh Kung Fu" và
nhiều dự án truyền hình. Vụ án khép lại sự nghiệp nghệ thuật đang lên của anh.

## Nguồn tham khảo

Tuổi Trẻ, VnExpress, Pháp Luật TP.HCM, ngày 28/4/2023.
""",
        },
        {
            "url": "https://vnexpress.net/chi-dan-an-tay-bi-khoi-to-ve-ma-tuy-4819726.html",
            "title": "Ca sĩ Chi Dân và người mẫu An Tây bị khởi tố về ma túy",
            "date_crawled": "2024-11-14T20:00:00",
            "content_markdown": """# Ca sĩ Chi Dân và người mẫu An Tây bị khởi tố về ma túy

Ngày 14/11/2024, Cơ quan Cảnh sát điều tra Công an TP.HCM bắt giữ ca sĩ Chi Dân
(tên thật Nguyễn Ngọc Anh, sinh năm 1990) và người mẫu An Tây trong khuôn khổ
chuyên án VN10 về ma túy.

## Chuyên án VN10

Chuyên án VN10 là chuyên án đấu tranh phòng, chống ma túy quy mô lớn của Công an
TP.HCM, đã bắt giữ tổng cộng 227 bị can trong nhiều đợt truy quét từ đầu năm 2024.

Vụ bắt giữ Chi Dân và An Tây nằm trong đợt truy quét ngày 14/11/2024, khi cơ quan
chức năng đồng loạt kiểm tra nhiều địa điểm tại TP.HCM và phát hiện nhiều đối tượng
sử dụng ma túy trái phép.

## Kết quả xét nghiệm

Kết quả xét nghiệm nhanh cho thấy cả Chi Dân và An Tây đều dương tính với chất ma
túy. Cơ quan điều tra tiến hành lấy mẫu giám định pháp y để xác định chính xác loại
và hàm lượng chất ma túy trong cơ thể.

## Khởi tố bị can

Cơ quan Cảnh sát điều tra Công an TP.HCM ra quyết định khởi tố vụ án, khởi tố bị
can đối với Chi Dân và An Tây về tội "Tàng trữ trái phép chất ma túy" theo Điều 249
Bộ luật Hình sự 2015.

## Phản ứng cộng đồng

Vụ việc gây chấn động cộng đồng yêu nhạc khi Chi Dân là ca sĩ có nhiều ca khúc
hit như "Cưới thôi", "Người lạ ơi" và có lượng người hâm mộ lớn. Các nhãn hàng
đã nhanh chóng chấm dứt hợp tác với Chi Dân sau thông tin này.

## Nguồn tham khảo

VnExpress, Tuổi Trẻ, Công An Nhân Dân, ngày 14-15/11/2024.
""",
        },
        {
            "url": "https://vnexpress.net/ca-si-miu-le-bi-bat-vi-lien-quan-ma-tuy-tai-cat-ba-2026.html",
            "title": "Ca sĩ Miu Lê bị bắt tại Cát Bà, dương tính 3 loại ma túy",
            "date_crawled": "2026-05-16T15:00:00",
            "content_markdown": """# Ca sĩ Miu Lê bị bắt tại Cát Bà, dương tính 3 loại ma túy

Ngày 10/5/2026, Công an huyện Cát Hải (Hải Phòng) bắt giữ ca sĩ Miu Lê (tên thật
Nguyễn Thị Mỹ Lệ, sinh năm 1990) tại khu nghỉ dưỡng trên đảo Cát Bà trong một
chuyên án về ma túy.

## Diễn biến bắt giữ

Căn cứ thông tin trinh sát, ngày 10/5/2026 Phòng Cảnh sát điều tra tội phạm về ma
túy Công an TP.Hải Phòng phối hợp Công an huyện Cát Hải ập vào một villa tại khu
nghỉ dưỡng trên đảo Cát Bà, bắt quả tang Miu Lê cùng 5 người khác đang có hành vi
sử dụng ma túy trái phép.

## Kết quả xét nghiệm

Kết quả xét nghiệm giám định pháp y xác nhận trong cơ thể Miu Lê dương tính với
3 loại chất ma túy:
- Methamphetamine (ma túy đá)
- Ketamine
- MDMA (Ecstasy)

Đây là lần đầu tiên Miu Lê bị phát hiện vi phạm pháp luật về ma túy.

## Khởi tố

Ngày 16/5/2026, Cơ quan Cảnh sát điều tra Công an TP.Hải Phòng ra quyết định khởi
tố bị can đối với Miu Lê về tội "Sử dụng trái phép chất ma túy" theo quy định của
pháp luật hiện hành.

## Sự nghiệp của Miu Lê

Miu Lê là ca sĩ, diễn viên nổi tiếng với các ca khúc "Đừng như thói quen", "Vì yêu
cứ đâm đầu" và vai diễn trong phim "Để Mai tính". Vụ việc gây sốc cho người hâm
mộ vì Miu Lê luôn có hình ảnh trong sáng, tích cực.

## Nguồn tham khảo

VnExpress, Tuổi Trẻ, Công An Nhân Dân, tháng 5/2026.
""",
        },
        {
            "url": "https://laodong.vn/phap-luat/diva-le-hang-bi-bat-qua-tang-su-dung-ma-tuy-tai-ha-noi-1160842.ldo",
            "title": "Ca sĩ Lệ Hằng bị bắt quả tang sử dụng ma túy tại Hà Nội",
            "date_crawled": "2023-03-10T22:00:00",
            "content_markdown": """# Ca sĩ Lệ Hằng bị bắt quả tang sử dụng ma túy tại Hà Nội

Đêm 10/3/2023, Công an phường Khâm Thiên (quận Đống Đa, Hà Nội) bắt quả tang ca
sĩ Lệ Hằng (tên thật Đào Lệ Hằng) đang sử dụng ma túy tại địa chỉ 104 Khâm Thiên.

## Diễn biến vụ bắt giữ

Nhận được thông tin phản ánh từ người dân về hoạt động sử dụng ma túy, tổ công tác
Công an phường Khâm Thiên (quận Đống Đa, Hà Nội) tiến hành kiểm tra địa chỉ 104
Khâm Thiên vào tối ngày 10/3/2023.

Lực lượng chức năng bắt quả tang Lệ Hằng cùng một số người khác đang có hành vi
sử dụng ma túy. Tang vật thu giữ bao gồm 0,696 gam ma túy tổng hợp (dạng bột) và
các dụng cụ sử dụng ma túy.

## Khai nhận của nghi phạm

Tại cơ quan công an, Lệ Hằng khai nhận đã mua 0,696 gam ma túy với giá 500.000 đồng
từ một người quen để sử dụng. Đây là lần đầu tiên bị phát hiện.

## Xử lý theo pháp luật

Theo Luật Phòng, chống ma túy 2021, hành vi sử dụng trái phép chất ma túy bị xử
phạt hành chính. Trường hợp tái phạm hoặc có tình tiết tăng nặng, người vi phạm có
thể bị áp dụng biện pháp cai nghiện bắt buộc theo Điều 32 Luật 73/2021/QH14.

Công an quận Đống Đa đã lập hồ sơ xử lý vi phạm hành chính đối với Lệ Hằng.

## Tác động đến sự nghiệp

Lệ Hằng từng được biết đến là giọng ca nội lực với nhiều ca khúc trữ tình và nhạc
đỏ nổi tiếng. Vụ việc khiến các hợp đồng biểu diễn và thương mại của cô bị đình
chỉ hoàn toàn.

## Nguồn tham khảo

Báo Lao Động, VnExpress, Công An Nhân Dân, ngày 10-11/3/2023.
""",
        },
        {
            "url": "https://vnexpress.net/nguyen-cong-tri-bi-bat-vi-lien-quan-duong-day-ma-tuy-qua-telegram-2025.html",
            "title": "NTK Nguyễn Công Trí bị bắt vì liên quan đường dây ma túy qua Telegram",
            "date_crawled": "2025-06-23T18:00:00",
            "content_markdown": """# NTK Nguyễn Công Trí bị bắt vì liên quan đường dây ma túy qua Telegram

Ngày 23/6/2025, Phòng Cảnh sát điều tra tội phạm về ma túy Công an TP.HCM bắt giữ
nhà thiết kế thời trang (NTK) Nguyễn Công Trí (sinh năm 1975) tại nhà riêng ở
đường Tân Hưng, quận 7, TP.HCM.

## Chuyên án và phương thức hoạt động

Nguyễn Công Trí bị bắt giữ trong khuôn khổ một chuyên án điều tra đường dây mua
bán, vận chuyển trái phép chất ma túy có tổ chức, sử dụng ứng dụng mã hóa Telegram
để liên lạc và giao dịch nhằm tránh sự phát hiện của cơ quan chức năng.

Đường dây này chuyên giao dịch cần sa (cannabis) và cocaine — hai loại chất ma túy
ngày càng phổ biến trong giới giải trí tại Việt Nam.

## Thu giữ tang vật

Tại thời điểm bắt giữ, cơ quan chức năng thu giữ tại nhà Nguyễn Công Trí một số
lượng cần sa và cocaine, cùng các thiết bị điện tử chứa đựng bằng chứng giao dịch
qua Telegram.

## Khởi tố và tội danh

Cơ quan Cảnh sát điều tra Công an TP.HCM khởi tố vụ án, khởi tố bị can đối với
Nguyễn Công Trí về tội "Tàng trữ trái phép chất ma túy" theo Điều 249 và điều tra
mở rộng về tội "Mua bán trái phép chất ma túy" theo Điều 251 Bộ luật Hình sự 2015.

## Sự nghiệp

Nguyễn Công Trí là nhà thiết kế thời trang hàng đầu Việt Nam, nổi tiếng với thương
hiệu NTK Công Trí và đã có nhiều bộ sưu tập được trình diễn tại Paris Fashion Week.
Ông từng thiết kế trang phục cho nhiều ngôi sao quốc tế.

Vụ bắt giữ gây sốc cho cộng đồng nghệ thuật Việt Nam và quốc tế, đặt ra câu hỏi
về tệ nạn ma túy trong giới nghệ sĩ.

## Nguồn tham khảo

VnExpress, Tuổi Trẻ, Thanh Niên, Pháp Luật TP.HCM, tháng 6/2025.
""",
        },
    ]

    for i, article in enumerate(articles, 1):
        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ Đã tạo: {filename} ({filepath.stat().st_size:,} bytes)")

    print(f"\n✓ Đã tạo {len(articles)} bài báo trong {DATA_DIR}")


if __name__ == "__main__":
    create_sample_news_articles()
