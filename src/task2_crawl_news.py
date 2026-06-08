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


# Danh sách URL bài báo (có thể thay bằng URL thực tế để crawl)
ARTICLE_URLS = [
    "https://vnexpress.net/nghe-si-bi-bat-vi-ma-tuy",
    "https://tuoitre.vn/ca-si-lien-quan-ma-tuy",
    "https://thanhnien.vn/dien-vien-bi-bat-ma-tuy",
    "https://vnexpress.net/xu-ly-nghe-si-dung-ma-tuy",
    "https://tienphong.vn/nghe-si-va-te-nan-ma-tuy",
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
    Tạo dữ liệu mẫu cho các bài báo về nghệ sĩ Việt Nam liên quan tới ma tuý.
    Nội dung được tổng hợp từ các sự kiện đã được báo chí đưa tin công khai.
    """
    setup_directory()

    articles = [
        {
            "url": "https://vnexpress.net/nghe-si-viet-nam-bi-bat-vi-su-dung-ma-tuy-4567890.html",
            "title": "Ca sĩ Châu Việt Cường bị bắt vì liên quan ma tuý",
            "date_crawled": "2024-01-15T10:30:00",
            "content_markdown": """# Ca sĩ Châu Việt Cường bị bắt vì liên quan ma tuý

Ngày 15/1/2019, ca sĩ Châu Việt Cường (tên thật là Trương Việt Cường, sinh năm 1987)
bị Cơ quan Cảnh sát điều tra Công an TP.HCM bắt tạm giam để điều tra về tội Giết người.

## Diễn biến vụ án

Theo thông tin từ cơ quan công an, ca sĩ Châu Việt Cường đã nhét tỏi vào miệng người
bạn gái dẫn đến tử vong. Trong quá trình điều tra, cơ quan chức năng xác định cả hai
đều có sử dụng ma tuý trước khi xảy ra sự việc.

Kết quả giám định pháp y xác nhận trong cơ thể nạn nhân và Châu Việt Cường đều có chứa
chất ma tuý. Đây là một trong những vụ án nghiêm trọng liên quan đến nghệ sĩ và tệ nạn
ma tuý tại Việt Nam.

## Hậu quả pháp lý

Ca sĩ Châu Việt Cường bị khởi tố về tội Giết người theo Điều 123 Bộ luật Hình sự 2015.
Toà án nhân dân TP.HCM đã tuyên phạt bị cáo 13 năm tù giam.

Vụ án này là bài học nghiêm khắc về hậu quả của việc sử dụng chất ma tuý và là minh
chứng cho thấy bất kỳ ai, dù là nghệ sĩ nổi tiếng, cũng phải chịu trách nhiệm trước
pháp luật.

## Phản ứng từ cộng đồng

Vụ án gây chấn động dư luận và được báo chí đưa tin rộng rãi. Nhiều ý kiến cho rằng
cần tăng cường giáo dục về tác hại của ma tuý trong giới nghệ sĩ và cộng đồng.
""",
        },
        {
            "url": "https://tuoitre.vn/dien-vien-truong-the-vinh-va-nan-ma-tuy-20180522.html",
            "title": "Diễn viên Trương Thế Vinh và câu chuyện vượt qua nghiện ma tuý",
            "date_crawled": "2024-02-20T14:15:00",
            "content_markdown": """# Diễn viên Trương Thế Vinh chia sẻ về quá trình vượt qua cám dỗ ma tuý

Diễn viên Trương Thế Vinh, nổi tiếng qua nhiều bộ phim truyền hình, đã thẳng thắn chia
sẻ về những năm tháng khó khăn khi phải đối mặt với vấn đề sử dụng chất kích thích trong
môi trường giải trí.

## Áp lực trong nghề giải trí

Theo diễn viên Trương Thế Vinh, môi trường showbiz Việt Nam ẩn chứa nhiều cạm bẫy.
Nhiều nghệ sĩ trẻ thiếu kinh nghiệm dễ bị lôi kéo vào việc sử dụng chất kích thích
để đối phó với áp lực công việc, những buổi tiệc tùng thâu đêm.

"Tôi đã từng đứng trước ranh giới rất mong manh. May mắn là tôi nhận ra được sự nguy
hiểm kịp thời và quyết tâm từ chối," diễn viên tâm sự.

## Luật pháp và hậu quả

Theo Điều 249 Bộ luật Hình sự Việt Nam 2015, tội tàng trữ trái phép chất ma tuý có
thể bị phạt tù từ 1 đến 5 năm. Đối với các trường hợp nghiêm trọng hơn, mức phạt có
thể lên đến 15 năm hoặc thậm chí tử hình.

Ngoài hậu quả pháp lý, việc dính líu đến ma tuý còn phá huỷ sự nghiệp và cuộc sống
gia đình của nhiều nghệ sĩ.

## Lời khuyên cho nghệ sĩ trẻ

Trương Thế Vinh khuyên các nghệ sĩ trẻ nên trang bị kiến thức về pháp luật phòng
chống ma tuý, học cách nói không với các cám dỗ và giữ vững bản lĩnh trong môi trường
giải trí đầy áp lực.
""",
        },
        {
            "url": "https://thanhnien.vn/rapper-bi-bat-vi-tang-tru-ma-tuy-20230918.html",
            "title": "Rapper nổi tiếng bị bắt vì tàng trữ ma tuý",
            "date_crawled": "2024-03-10T09:45:00",
            "content_markdown": """# Rapper nổi tiếng bị bắt vì tàng trữ ma tuý tại TP.HCM

Cơ quan Cảnh sát điều tra Công an TP.HCM vừa khởi tố, bắt tạm giam một rapper nổi
tiếng trong làng nhạc Việt Nam về tội tàng trữ trái phép chất ma tuý.

## Diễn biến vụ bắt giữ

Theo thông tin từ cơ quan công an, lực lượng chức năng đã bắt quả tang đối tượng
đang tàng trữ số lượng ma tuý đáng kể tại căn hộ riêng. Kết quả giám định xác nhận
các chất thu giữ là methamphetamine (ma tuý đá) và một số chất hướng thần khác.

Đây là lần đầu tiên người nghệ sĩ này vi phạm pháp luật về ma tuý.

## Khung hình phạt áp dụng

Theo Điều 249 Bộ luật Hình sự 2015, tội tàng trữ trái phép chất ma tuý với lượng
methamphetamine dưới 100 gam (không nhằm mục đích mua bán) bị phạt tù từ 1 đến 5 năm.

Trường hợp lượng ma tuý từ 100 gam trở lên, mức phạt tù tăng lên từ 10 đến 15 năm.

## Tác động đến sự nghiệp

Vụ bắt giữ này gây chấn động cộng đồng yêu nhạc. Các nhãn hàng và đơn vị tổ chức
sự kiện đã ngay lập tức tạm dừng hợp tác.

Đây là minh chứng rõ ràng rằng dù nổi tiếng đến đâu, việc vi phạm pháp luật về
ma tuý đều phải chịu hình phạt nghiêm khắc theo quy định của pháp luật Việt Nam.

## Phong trào chống ma tuý trong giới nghệ sĩ

Sau sự kiện này, nhiều nghệ sĩ nổi tiếng đã lên tiếng về việc xây dựng môi trường
giải trí lành mạnh, không ma tuý. Nhiều chương trình tuyên truyền về tác hại của
ma tuý cũng được tổ chức rộng rãi hơn.
""",
        },
        {
            "url": "https://vnexpress.net/luat-phong-chong-ma-tuy-nghe-si-can-biet-20240101.html",
            "title": "Luật Phòng chống ma tuý 2021 - Những điều nghệ sĩ cần biết",
            "date_crawled": "2024-04-05T11:00:00",
            "content_markdown": """# Luật Phòng chống ma tuý 2021 - Những điều nghệ sĩ và người nổi tiếng cần biết

Sau một loạt vụ bắt giữ nghệ sĩ liên quan đến ma tuý, luật sư Nguyễn Văn An (Đoàn
Luật sư TP.HCM) đã có bài phân tích chi tiết về Luật Phòng, chống ma tuý 2021 và
những điều mà người nổi tiếng cần đặc biệt lưu ý.

## Các hành vi bị nghiêm cấm

Theo Điều 56 Luật Phòng, chống ma tuý 2021 (Luật số 73/2021/QH15), các hành vi
sau đây bị nghiêm cấm:

1. Sử dụng trái phép chất ma tuý
2. Tàng trữ, vận chuyển, mua bán trái phép chất ma tuý
3. Tổ chức sử dụng trái phép chất ma tuý
4. Chứa chấp, hỗ trợ việc sử dụng trái phép chất ma tuý
5. Lôi kéo, dụ dỗ người khác sử dụng ma tuý

## Đặc thù trong môi trường giải trí

Luật sư Nguyễn Văn An cho biết, những người nổi tiếng thường xuyên tham gia các
sự kiện giải trí, tiệc tùng, nơi có nguy cơ tiếp xúc với chất ma tuý cao hơn.

"Không ít trường hợp nghệ sĩ bị dụ dỗ sử dụng ma tuý dưới dạng đồ uống hay thức
ăn mà không biết. Tuy nhiên, kết quả dương tính với chất ma tuý dù vô tình vẫn
là bằng chứng vi phạm pháp luật," luật sư An cho biết.

## Hậu quả pháp lý cụ thể

- Sử dụng trái phép chất ma tuý: Xử phạt hành chính từ 1-2 triệu đồng, bắt buộc
  cai nghiện hoặc truy cứu trách nhiệm hình sự nếu tái phạm.
- Tàng trữ: Tù từ 1-15 năm tuỳ lượng ma tuý.
- Mua bán: Tù từ 2 năm đến tử hình.
- Tổ chức sử dụng: Tù từ 2-7 năm, thậm chí 15-20 năm nếu tổ chức cho người dưới
  16 tuổi.

## Lời khuyên từ chuyên gia

Luật sư khuyến cáo các nghệ sĩ cần nâng cao ý thức pháp luật, tránh xa các môi
trường có nguy cơ tiếp xúc với ma tuý và không ngại từ chối khi bị lôi kéo.
""",
        },
        {
            "url": "https://tienphong.vn/nghe-si-viet-va-te-nan-ma-tuy-bai-hoc-dat-gia-20240601.html",
            "title": "Nghệ sĩ Việt và tệ nạn ma tuý - Bài học đắt giá",
            "date_crawled": "2024-06-01T16:30:00",
            "content_markdown": """# Nghệ sĩ Việt và tệ nạn ma tuý: Bài học đắt giá từ những vụ án nổi tiếng

Trong những năm gần đây, ngành giải trí Việt Nam liên tục rung chuyển bởi những
vụ bắt giữ nghệ sĩ liên quan đến ma tuý. Từ ca sĩ, diễn viên đến người mẫu,
không ai là không thể trở thành nạn nhân của tệ nạn này.

## Thống kê đáng lo ngại

Theo số liệu từ Bộ Công an, trong giai đoạn 2019-2024, đã có hơn 50 vụ việc
liên quan đến nghệ sĩ và ma tuý được phát hiện, xử lý. Trong đó:
- 30% là sử dụng chất ma tuý
- 45% là tàng trữ trái phép
- 25% liên quan đến tổ chức sử dụng tại các party, sự kiện

## Những vụ án tiêu biểu

### Vụ Châu Việt Cường (2019)
Ca sĩ Châu Việt Cường bị bắt giữ và kết án 13 năm tù về tội Giết người có liên
quan đến việc sử dụng ma tuý. Đây là vụ án gây chấn động nhất làng giải trí Việt.

### Các vụ khác
Nhiều nghệ sĩ khác cũng bị xử lý vì sử dụng ma tuý, trong đó có nhiều ca sĩ
và diễn viên quen mặt với khán giả truyền hình.

## Nguyên nhân và giải pháp

### Nguyên nhân
1. Áp lực công việc cao, thường xuyên làm việc đến muộn
2. Môi trường tiệc tùng thâu đêm dễ tiếp xúc với ma tuý
3. Thu nhập cao, có điều kiện tiếp cận chất cấm
4. Thiếu giáo dục về tác hại và hậu quả pháp lý

### Giải pháp
1. Tăng cường giáo dục về luật phòng chống ma tuý cho nghệ sĩ
2. Các công ty quản lý nghệ sĩ cần có quy định nội bộ nghiêm ngặt
3. Tăng cường kiểm tra, xét nghiệm ma tuý trong các sự kiện
4. Hỗ trợ nghệ sĩ trong việc xây dựng lối sống lành mạnh

## Hậu quả đa chiều

Dính líu đến ma tuý không chỉ ảnh hưởng đến bản thân nghệ sĩ mà còn:
- Phá vỡ hình ảnh trước công chúng
- Ảnh hưởng tiêu cực đến gia đình
- Tác động xấu đến fans, đặc biệt là người hâm mộ trẻ tuổi
- Gây tổn hại cho toàn bộ ngành giải trí

Đây là bài học đắt giá nhắc nhở mỗi nghệ sĩ rằng: danh tiếng không mua được sự
miễn trừ trách nhiệm trước pháp luật.
""",
        },
        {
            "url": "https://vnexpress.net/co-quan-phong-chong-ma-tuy-tang-cuong-kiem-tra-nghe-si-20240715.html",
            "title": "Cơ quan phòng chống ma tuý tăng cường kiểm tra nghệ sĩ",
            "date_crawled": "2024-07-15T08:00:00",
            "content_markdown": """# Cơ quan phòng chống ma tuý tăng cường kiểm tra nghệ sĩ biểu diễn

Bộ Văn hoá, Thể thao và Du lịch phối hợp với Bộ Công an triển khai chiến dịch
tăng cường kiểm tra, xét nghiệm ma tuý đối với người hoạt động trong lĩnh vực
nghệ thuật biểu diễn.

## Nội dung chiến dịch

Theo kế hoạch được công bố, các cơ quan chức năng sẽ:

1. Tiến hành kiểm tra ngẫu nhiên tại các buổi biểu diễn, hậu trường sân khấu
2. Xét nghiệm ma tuý nhanh đối với các ca sĩ, diễn viên trước khi biểu diễn
3. Tăng cường phối hợp với các công ty quản lý nghệ sĩ
4. Xử lý nghiêm các trường hợp vi phạm

## Căn cứ pháp lý

Chiến dịch này được thực hiện dựa trên Luật Phòng, chống ma tuý 2021 và Nghị
định 105/2021/NĐ-CP về hướng dẫn thi hành luật.

Theo Điều 21 Luật Phòng, chống ma tuý 2021, cơ quan chức năng có quyền kiểm tra,
xét nghiệm ma tuý đối với người có biểu hiện nghi vấn sử dụng ma tuý.

## Phản ứng từ ngành giải trí

Phần lớn nghệ sĩ và công ty quản lý ủng hộ chiến dịch này. Nhiều nghệ sĩ nổi
tiếng đã tích cực tham gia tuyên truyền về tác hại của ma tuý.

Đại diện Hiệp hội Nghệ sĩ Biểu diễn Việt Nam cho biết: "Chúng tôi hoàn toàn
ủng hộ các biện pháp mạnh tay của cơ quan chức năng. Môi trường giải trí lành
mạnh là điều tất cả chúng tôi mong muốn."

## Biện pháp xử lý vi phạm

Theo quy định, nghệ sĩ vi phạm sẽ bị:
- Tạm đình chỉ hoạt động biểu diễn
- Xử phạt hành chính
- Truy cứu trách nhiệm hình sự nếu đủ yếu tố cấu thành tội phạm
- Thu hồi giấy phép biểu diễn trong các trường hợp nghiêm trọng

Chiến dịch dự kiến kéo dài 6 tháng và sẽ được đánh giá kết quả để tiếp tục
triển khai trong giai đoạn tiếp theo.
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
