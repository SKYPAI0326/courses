from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "photos"
OUT.mkdir(parents=True, exist_ok=True)
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size: int, index: int = 0):
    return ImageFont.truetype(FONT_PATH, size=size, index=index)


def photo_canvas():
    image = Image.new("RGB", (1600, 1200), (239, 226, 203))
    draw = ImageDraw.Draw(image)
    for x in range(0, 1600, 80):
        draw.line((x, 0, x - 180, 1200), fill=(231, 214, 187), width=2)
    for y in range(0, 1200, 80):
        draw.line((0, y, 1600, y + 260), fill=(244, 233, 215), width=2)
    return image


def place_document(base, document, angle=2, center=(800, 600)):
    shadow = Image.new("RGBA", document.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((22, 24, document.width - 8, document.height - 6), 18, fill=(55, 40, 28, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18)).rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    shadow_pos = (center[0] - shadow.width // 2 + 12, center[1] - shadow.height // 2 + 20)
    base.paste(shadow, shadow_pos, shadow)
    rotated = document.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    pos = (center[0] - rotated.width // 2, center[1] - rotated.height // 2)
    base.paste(rotated, pos, rotated)


def new_document(size=(1220, 820), background=(255, 255, 252)):
    doc = Image.new("RGBA", size, background + (255,))
    draw = ImageDraw.Draw(doc)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), 18, outline=(208, 201, 188), width=3)
    return doc, draw


def save_quotation():
    doc, draw = new_document()
    draw.rectangle((0, 0, 1220, 112), fill=(35, 85, 76))
    draw.text((46, 26), "青禾包材有限公司", font=font(42, 1), fill="white")
    draw.text((900, 34), "報價單 Q-2026-031", font=font(25), fill="white")
    draw.text((46, 144), "客戶：午後咖啡館（虛構練習資料）", font=font(28), fill=(36, 45, 43))
    draw.text((46, 190), "日期：2026-08-25　有效期限：7 日", font=font(25), fill=(80, 83, 78))
    top = 260
    cols = [46, 430, 650, 830, 1035]
    headers = ["品項", "規格", "數量", "單價", "小計"]
    draw.rectangle((42, top - 8, 1176, top + 58), fill=(231, 241, 235))
    for x, text in zip(cols, headers):
        draw.text((x, top + 8), text, font=font(25, 1), fill=(28, 66, 55))
    rows = [
        ("外帶杯", "12oz 紙杯", "500", "4.8", "2,400"),
        ("杯蓋", "通用款", "500", "2.1", "1,050"),
        ("貼紙", "圓形 5cm", "200", "3.5", "700"),
    ]
    for row_i, row in enumerate(rows):
        y = top + 82 + row_i * 76
        draw.line((44, y - 17, 1174, y - 17), fill=(219, 217, 209), width=2)
        for x, text in zip(cols, row):
            draw.text((x, y), text, font=font(24), fill=(49, 54, 50))
    draw.line((44, 590, 1174, 590), fill=(122, 137, 129), width=3)
    draw.text((785, 620), "未稅合計　4,150 元", font=font(28, 1), fill=(35, 85, 76))
    draw.text((46, 676), "備註：交期與運費請於下單前再次確認。", font=font(23), fill=(90, 87, 78))
    draw.text((46, 728), "虛構練習資料｜OCR 欄位抽取用｜不得對外使用", font=font(22, 1), fill=(174, 66, 51))
    base = photo_canvas()
    place_document(base, doc, 2, (800, 590))
    base.save(OUT / "ch1-3-quotation-photo.jpg", quality=92, optimize=True)


def save_card():
    doc, draw = new_document((1220, 720), (248, 252, 244))
    draw.rectangle((0, 0, 1220, 720), fill=(249, 252, 244))
    draw.rectangle((0, 0, 18, 720), fill=(83, 126, 95))
    draw.ellipse((86, 112, 300, 326), fill=(224, 237, 222), outline=(83, 126, 95), width=5)
    draw.text((137, 158), "森", font=font(86, 1), fill=(58, 105, 74))
    draw.text((380, 112), "森日花藝工作室", font=font(50, 1), fill=(44, 75, 56))
    draw.text((384, 196), "一束花，替日常留一個呼吸。", font=font(27), fill=(91, 102, 90))
    draw.line((384, 264, 1128, 264), fill=(185, 207, 184), width=3)
    fields = [
        "聯絡人：林沐（虛構）",
        "電話：02-0000-1234",
        "Email：hello@example.test",
        "地址：台北市示範區練習路 10 號",
    ]
    for i, text in enumerate(fields):
        draw.text((384, 322 + i * 58), text, font=font(27), fill=(51, 67, 54))
    draw.text((86, 630), "虛構練習資料｜OCR 欄位抽取用｜不得對外使用", font=font(22, 1), fill=(174, 66, 51))
    base = photo_canvas()
    place_document(base, doc, -1.2, (800, 600))
    base.save(OUT / "ch1-3-business-card-photo.jpg", quality=92, optimize=True)


def save_menu():
    doc, draw = new_document((1220, 900), (255, 250, 239))
    draw.rectangle((0, 0, 1220, 900), fill=(255, 250, 239))
    draw.text((72, 52), "午後咖啡館", font=font(58, 1), fill=(91, 61, 44))
    draw.text((76, 132), "AFTERNOON COFFEE · MENU", font=font(25), fill=(157, 119, 89))
    draw.line((72, 194, 1148, 194), fill=(196, 164, 130), width=3)
    draw.text((76, 234), "咖啡", font=font(32, 1), fill=(91, 61, 44))
    items = [("美式咖啡", "100"), ("拿鐵咖啡", "140"), ("手沖單品", "180")]
    for i, (name, price) in enumerate(items):
        y = 300 + i * 64
        draw.text((96, y), name, font=font(28), fill=(70, 62, 55))
        draw.text((974, y), f"$ {price}", font=font(28, 1), fill=(70, 62, 55))
        draw.line((360, y + 23, 936, y + 23), fill=(226, 211, 191), width=2)
    draw.text((76, 520), "甜點", font=font(32, 1), fill=(91, 61, 44))
    sweets = [("原味司康", "80"), ("檸檬磅蛋糕", "120")]
    for i, (name, price) in enumerate(sweets):
        y = 586 + i * 64
        draw.text((96, y), name, font=font(28), fill=(70, 62, 55))
        draw.text((974, y), f"$ {price}", font=font(28, 1), fill=(70, 62, 55))
    draw.text((76, 790), "供應與活動價格請以店內最新公告為準。", font=font(22), fill=(105, 93, 78))
    draw.text((76, 838), "虛構練習資料｜OCR 欄位抽取用｜不得對外使用", font=font(22, 1), fill=(174, 66, 51))
    base = photo_canvas()
    place_document(base, doc, 1.1, (800, 600))
    base.save(OUT / "ch1-3-menu-photo.jpg", quality=92, optimize=True)


if __name__ == "__main__":
    save_quotation()
    save_card()
    save_menu()
    print("generated", *sorted(str(path) for path in OUT.glob("ch1-3-*-photo.jpg")), sep="\n")
