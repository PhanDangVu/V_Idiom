from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def load_font(size: int, bold: bool = False):
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/Library/Fonts/Arial Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
    )
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_rounded_box(draw, box, radius, fill, outline, width=4):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_card_with_header(draw, box, header_text, bullets, border_color, header_bg, body_bg, title_color):
    x1, y1, x2, y2 = box
    draw_rounded_box(draw, box, radius=22, fill=body_bg, outline=border_color, width=4)
    header_h = 66
    draw.line([(x1 + 24, y1 + header_h), (x2 - 24, y1 + header_h)], fill=header_bg, width=2)

    f_title = load_font(26, bold=True)
    f_body = load_font(22, bold=False)

    tb = draw.textbbox((0, 0), header_text, font=f_title)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    draw.text(((x1 + x2 - tw) / 2, y1 + (header_h - th) / 2 - 2), header_text, font=f_title, fill=title_color)

    avail_h = y2 - (y1 + header_h)
    step_y = avail_h / (len(bullets) + 1)
    for i, b in enumerate(bullets, 1):
        bb = draw.textbbox((0, 0), b, font=f_body)
        bw = bb[2] - bb[0]
        bh = bb[3] - bb[1]
        cy = y1 + header_h + i * step_y - bh / 2 - 2
        draw.text(((x1 + x2 - bw) / 2, cy), b, font=f_body, fill="#1e293b")


def draw_diamond(draw, cx, cy, rx, ry, fill, outline, title, subtitle, title_color="#7c2d12", sub_color="#78350f"):
    pts = [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
    draw.polygon(pts, fill=fill, outline=outline, width=5)
    f_t = load_font(23, bold=True)
    f_s = load_font(19, bold=False)
    tb = draw.textbbox((0, 0), title, font=f_t)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    draw.text((cx - tw / 2, cy - th - 5), title, font=f_t, fill=title_color)

    sb = draw.textbbox((0, 0), subtitle, font=f_s)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    draw.text((cx - sw / 2, cy + 7), subtitle, font=f_s, fill=sub_color)


def draw_arrow_down(draw, x, y1, y2, color="#334155", width=5):
    draw.line([(x, y1), (x, y2 - 14)], fill=color, width=width)
    draw.polygon([(x, y2), (x - 11, y2 - 18), (x + 11, y2 - 18)], fill=color)


def draw_pill_label(draw, cx, cy, text, border_color, text_color, fill="#ffffff"):
    f = load_font(19, bold=True)
    tb = draw.textbbox((0, 0), text, font=f)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 14, 7
    box = (cx - tw / 2 - pad_x, cy - th / 2 - pad_y, cx + tw / 2 + pad_x, cy + th / 2 + pad_y)
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=border_color, width=3)
    draw.text((cx - tw / 2, cy - th / 2 - 2), text, font=f, fill=text_color)


def main():
    W, H = 2500, 3360
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # Main Title & Subtitle
    f_main = load_font(42, bold=True)
    f_sub = load_font(25, bold=False)
    title_str = "FLOWCHART PHƯƠNG PHÁP LAI GHÉP: BẢN THỂ HỌC OWL 2 (v6) + TRANSFORMER"
    sub_str = "Tra cứu Ontology v-idiomV6.rdf kết hợp Đối sánh Khung & Mô hình Đa ngôn ngữ (LaBSE / BGE-M3)"

    tb = draw.textbbox((0, 0), title_str, font=f_main)
    draw.text((cx - (tb[2] - tb[0]) / 2, 50), title_str, font=f_main, fill="#0f172a")
    sb = draw.textbbox((0, 0), sub_str, font=f_sub)
    draw.text((cx - (sb[2] - sb[0]) / 2, 112), sub_str, font=f_sub, fill="#64748b")

    # STEP 1: INPUT PILL
    s1_box = (cx - 480, 175, cx + 480, 300)
    draw.rounded_rectangle(s1_box, radius=62, fill="#1d4ed8", outline="#1e40af", width=4)
    f_s1_t = load_font(30, bold=True)
    f_s1_s = load_font(23, bold=False)
    t1 = "1. NHẬP CÂU THÀNH NGỮ CẦN ĐỐI SÁNH"
    t1_sub = "(Từng câu độc lập: Tiếng Việt hoặc Tiếng Anh)"
    b1 = draw.textbbox((0, 0), t1, font=f_s1_t)
    b1s = draw.textbbox((0, 0), t1_sub, font=f_s1_s)
    draw.text((cx - (b1[2] - b1[0]) / 2, 200), t1, font=f_s1_t, fill="#ffffff")
    draw.text((cx - (b1s[2] - b1s[0]) / 2, 246), t1_sub, font=f_s1_s, fill="#dbeafe")

    # Arrow Step 1 -> Diamond 1
    draw_arrow_down(draw, cx, 300, 360)

    # DIAMOND 1: ĐÃ CÓ TRONG ONTOLOGY v-idiomV6.rdf?
    d1_cy = 470
    d1_rx, d1_ry = 440, 110
    draw_diamond(
        draw,
        cx=cx,
        cy=d1_cy,
        rx=d1_rx,
        ry=d1_ry,
        fill="#fef3c7",
        outline="#d97706",
        title="ĐÃ CÓ TRONG ONTOLOGY (v-idiomV6.rdf)?",
        subtitle="(Tra cứu trong 382 cá thể thành ngữ sẵn có)",
    )

    # Branch Left (2A: Đã có trong Ontology) & Right (2B: Câu mới -> Gọi LLM)
    left_cx = 560
    right_cx = 1940
    box2_y1, box2_y2 = 640, 900

    # Lines from Diamond 1 left & right
    draw.line([(cx - d1_rx, d1_cy), (left_cx, d1_cy)], fill="#0284c7", width=5)
    draw_arrow_down(draw, left_cx, d1_cy, box2_y1, color="#0284c7", width=5)
    draw_pill_label(draw, left_cx, d1_cy - 30, "CÓ SẴN TRONG ONTOLOGY", "#0284c7", "#0369a1")

    draw.line([(cx + d1_rx, d1_cy), (right_cx, d1_cy)], fill="#9333ea", width=5)
    draw_arrow_down(draw, right_cx, d1_cy, box2_y1, color="#9333ea", width=5)
    draw_pill_label(draw, right_cx, d1_cy - 30, "CÂU MỚI (CHƯA CÓ)", "#9333ea", "#7e22ce")

    # 2A Card (Left)
    draw_card_with_header(
        draw,
        box=(90, box2_y1, 1140, box2_y2),
        header_text="2A. LẤY TRỰC TIẾP TỪ ONTOLOGY (v-idiomV6.rdf)",
        bullets=[
            "• Không gọi LLM suy luận (Thời gian trích xuất: 0ms)",
            "• Lấy nguyên văn Description (rdfs:comment) thuần của câu đó",
            "• Lấy chính xác Khung# và 4 trục tiêu chí (BC, HD, KQ, MD) gốc",
        ],
        border_color="#0284c7",
        header_bg="#bae6fd",
        body_bg="#f0f9ff",
        title_color="#0369a1",
    )

    # 2B Card (Right)
    draw_card_with_header(
        draw,
        box=(1360, box2_y1, 2410, box2_y2),
        header_text="2B. SUY LUẬN NGHĨA BÓNG & TIÊU CHÍ (LLM Groq API)",
        bullets=[
            "• Giải mã lớp nghĩa bóng (Gloss) thuần túy của câu thành ngữ mới",
            "• Trích xuất 4 trục: Bối cảnh (BC), Hành động (HD), Kết quả (KQ), Mục đích (MD)",
            "• Chọn các tiêu chí khớp nhất từ Bể tiêu chí v5 (236 tiêu chí)",
        ],
        border_color="#9333ea",
        header_bg="#e9d5ff",
        body_bg="#faf5ff",
        title_color="#6b21a8",
    )

    # Merge 2A & 2B -> Step 3
    merge2_y = 945
    draw.line([(left_cx, box2_y2), (left_cx, merge2_y), (right_cx, merge2_y), (right_cx, box2_y2)], fill="#334155", width=5)
    draw_arrow_down(draw, cx, merge2_y, 995, color="#334155", width=5)

    # STEP 3: ĐỐI SOÁT KHUNG BẢN THỂ HỌC (S_onto)
    box3_y1, box3_y2 = 995, 1275
    draw_card_with_header(
        draw,
        box=(350, box3_y1, 2150, box3_y2),
        header_text="3. ĐỐI SOÁT KHUNG BẢN THỂ HỌC 4 TRỤC (TÍNH ĐIỂM S_onto)",
        bullets=[
            "• Trọng số 4 trục (BC, HD, KQ, MD) BẰNG NHAU: S_onto = (Tổng điểm khớp) / (Tổng số trục tiêu chí) — VD: 2/3 = 0.67, 2/4 = 0.50",
            "• Khớp chính xác mã tiêu chí (Exact Match): +1.0 điểm trên trục đó",
            "• Khớp nhóm tiêu chí liên quan (Related Group — Transformer mô tả tiêu chí >= 0.70): +0.75 điểm trên trục đó",
            "• Phủ quyết nhân quả (Veto): Phạt nặng nếu trùng Bối cảnh nhưng ngược hẳn Kết quả nhân-quả",
        ],
        border_color="#d97706",
        header_bg="#fde68a",
        body_bg="#fffbeb",
        title_color="#b45309",
    )

    # Arrow Step 3 -> Diamond 2
    draw_arrow_down(draw, cx, box3_y2, 1335)

    # DIAMOND 2: KHUNG TRÙNG HẾT 100% (S_onto == 1.0)?
    d2_cy = 1450
    d2_rx, d2_ry = 480, 115
    draw_diamond(
        draw,
        cx=cx,
        cy=d2_cy,
        rx=d2_rx,
        ry=d2_ry,
        fill="#dcfce7",
        outline="#16a34a",
        title="TRÙNG 100% KHUNG BẢN THỂ HỌC (S_onto = 1.0)?",
        subtitle="(Tất cả các trục tiêu chí BC, HD, KQ, MD trùng khớp hoàn toàn)",
        title_color="#14532d",
        sub_color="#166534",
    )

    # Left Fast-Track Branch: S_onto == 1.0 -> Straight down to Exact Synonym Box (No LaBSE needed!)
    fast_x = 220
    draw.line([(cx - d2_rx, d2_cy), (fast_x, d2_cy)], fill="#16a34a", width=6)
    draw_pill_label(
        draw,
        (cx - d2_rx + fast_x) / 2,
        d2_cy - 32,
        "S_onto = 1.0 (TRÙNG HẾT KHUNG)",
        "#16a34a",
        "#15803d",
    )

    # Downward branch for S_onto < 1.0 -> Step 4 (LaBSE)
    draw_arrow_down(draw, cx, d2_cy + d2_ry, 1640, color="#0284c7", width=5)
    draw_pill_label(draw, cx + 230, d2_cy + d2_ry + 35, "S_onto < 1.0 (Khung chưa trùng 100%)", "#0284c7", "#0369a1")

    # STEP 4: GHÉP CHUỖI NEO & MÃ HÓA VECTOR ĐA NGÔN NGỮ TRANSFORMER
    box4_y1, box4_y2 = 1640, 1910
    draw_card_with_header(
        draw,
        box=(440, box4_y1, 2180, box4_y2),
        header_text="4. GHÉP CHUỖI NEO & MÃ HÓA VECTOR ĐA NGÔN NGỮ (TRANSFORMER EMBEDDING)",
        bullets=[
            "• Ghép chuỗi neo Bản thể học: \"[Bối cảnh | Hành động | Kết quả | Mục đích] : <Nghĩa bóng Gloss thuần>\"",
            "• Mã hóa qua mô hình Transformer đa ngôn ngữ (LaBSE 768d hoặc BGE-M3 1024d) chuẩn hóa L2",
            "• Tính khoảng cách Cosine Similarity trên từng câu: S_Transformer ([Khung + Gloss]) và S_Gloss ([Gloss thuần])",
        ],
        border_color="#0284c7",
        header_bg="#bae6fd",
        body_bg="#f0f9ff",
        title_color="#0369a1",
    )

    # Arrow Step 4 -> Step 5
    draw_arrow_down(draw, cx, box4_y2, 1975)

    # STEP 5: TÍNH ĐIỂM TƯƠNG ĐỒNG LAI GHÉP (HYBRID SCORE) & BỘ LỌC SÀN
    box5_y1, box5_y2 = 1975, 2225
    draw_card_with_header(
        draw,
        box=(440, box5_y1, 2180, box5_y2),
        header_text="5. TÍNH ĐIỂM TƯƠNG ĐỒNG LAI GHÉP (S_hybrid) & LỌC SÀN NGỮ NGHĨA",
        bullets=[
            "• Công thức kết hợp Neuro-Symbolic: S_hybrid = 0.65 * S_Transformer + 0.35 * S_onto",
            "• Bộ lọc sàn ngữ nghĩa bắt buộc: S_Gloss >= 0.60 (Chặn các câu trùng khung giả nhưng khác nghĩa bóng)",
        ],
        border_color="#334155",
        header_bg="#cbd5e1",
        body_bg="#f8fafc",
        title_color="#0f172a",
    )

    # Arrow Step 5 -> Diamond 3
    draw_arrow_down(draw, cx, box5_y2, 2290)

    # DIAMOND 3: ĐÁNH GIÁ NGƯỠNG S_hybrid, S_onto & S_Gloss
    d3_cy = 2400
    d3_rx, d3_ry = 440, 110
    draw_diamond(
        draw,
        cx=cx,
        cy=d3_cy,
        rx=d3_rx,
        ry=d3_ry,
        fill="#ffedd5",
        outline="#d97706",
        title="ĐÁNH GIÁ NGƯỠNG ĐỒNG NGHĨA?",
        subtitle="(Kết hợp S_hybrid, S_onto và S_Gloss >= 0.60)",
    )

    # 3 Outcome Cards at y = 2620..2955
    out_y1, out_y2 = 2620, 2955
    b_left = (80, out_y1, 820, out_y2)
    b_mid = (880, out_y1, 1620, out_y2)
    b_right = (1680, out_y1, 2420, out_y2)

    # Connect Fast-Track (S_onto == 1.0) straight into Left Card (ĐỒNG NGHĨA CỨNG / TUYỆT ĐỐI)
    draw.line([(fast_x, d2_cy), (fast_x, out_y1 - 14)], fill="#16a34a", width=6)
    draw.polygon([(fast_x, out_y1), (fast_x - 12, out_y1 - 20), (fast_x + 12, out_y1 - 20)], fill="#16a34a")
    draw_pill_label(
        draw,
        fast_x + 10,
        1950,
        "ĐỒNG NGHĨA CỨNG LUÔN (BỎ QUA TRANSFORMER)",
        "#16a34a",
        "#15803d",
        fill="#f0fdf4",
    )

    # Connect Diamond 3 Left -> Left Card (at x = 580)
    left_in_x = 580
    draw.line([(cx - d3_rx, d3_cy), (left_in_x, d3_cy)], fill="#16a34a", width=5)
    draw_arrow_down(draw, left_in_x, d3_cy, out_y1, color="#16a34a", width=5)
    draw_pill_label(
        draw,
        left_in_x,
        d3_cy + 95,
        "S_hybrid >= 0.80 & S_onto >= 0.75 & S_Gloss >= 0.60",
        "#16a34a",
        "#15803d",
    )

    # Connect Diamond 3 Down -> Middle Card (at x = cx)
    draw_arrow_down(draw, cx, d3_cy + d3_ry, out_y1, color="#0284c7", width=5)
    draw_pill_label(
        draw,
        cx,
        d3_cy + d3_ry + 48,
        "0.62 <= S_hybrid < 0.80 & S_onto >= 0.50 & S_Gloss >= 0.60",
        "#0284c7",
        "#0369a1",
    )

    # Connect Diamond 3 Right -> Right Card (at x = 2050)
    right_in_x = 2050
    draw.line([(cx + d3_rx, d3_cy), (right_in_x, d3_cy)], fill="#dc2626", width=5)
    draw_arrow_down(draw, right_in_x, d3_cy, out_y1, color="#dc2626", width=5)
    draw_pill_label(
        draw,
        right_in_x,
        d3_cy + 95,
        "S_Gloss < 0.60 hoặc S_onto < 0.50 hoặc S_hybrid < 0.62",
        "#dc2626",
        "#b91c1c",
    )

    # Left Outcome Card: ĐỒNG NGHĨA CỨNG / TUYỆT ĐỐI
    draw_card_with_header(
        draw,
        box=b_left,
        header_text="ĐỒNG NGHĨA CỨNG / TUYỆT ĐỐI",
        bullets=[
            "• TH1: Trùng 100% Khung (S_onto = 1.0) -> Đồng nghĩa cứng luôn",
            "• TH2: S_hybrid >= 0.80, S_onto >= 0.75 & S_Gloss >= 0.60",
            "• Gán trực tiếp vào Khung Bản thể học sẵn có",
            "• Xuất các câu thành ngữ Việt / Anh tương đương",
        ],
        border_color="#16a34a",
        header_bg="#bbf7d0",
        body_bg="#f0fdf4",
        title_color="#15803d",
    )

    # Middle Outcome Card: ĐỒNG NGHĨA MỀM (CẬN NGHĨA)
    draw_card_with_header(
        draw,
        box=b_mid,
        header_text="ĐỒNG NGHĨA MỀM (CẬN NGHĨA)",
        bullets=[
            "• S_onto >= 0.50, S_Gloss >= 0.60 và 0.62 <= S_hybrid < 0.80",
            "• Cứu các câu lệch nhẹ tiêu chí hoặc thuộc Related Group",
            "• (Tiêu chí có Transformer >= 0.70 được nhân hệ số +0.75)",
            "• Gợi ý danh sách từng câu thành ngữ gần nghĩa nhất",
        ],
        border_color="#0284c7",
        header_bg="#bae6fd",
        body_bg="#f0f9ff",
        title_color="#0369a1",
    )

    # Right Outcome Card: KHÁC NGHĨA / LOẠI TRÙNG KHUNG GIẢ
    draw_card_with_header(
        draw,
        box=b_right,
        header_text="KHÁC NGHĨA / KHUNG MỚI",
        bullets=[
            "• Chặn các câu trùng khung giả nhưng S_Gloss < 0.60",
            "• Loại bỏ các câu khác cấu trúc (S_onto < 0.50)",
            "• Khởi tạo Khung Bản thể học mới (nếu chưa tồn tại)",
            "• Mở rộng tri thức vào Ontology v-idiomV6.rdf",
        ],
        border_color="#dc2626",
        header_bg="#fecaca",
        body_bg="#fef2f2",
        title_color="#b91c1c",
    )

    # Merge 3 Outcome Cards -> Step 6
    merge6_y = 3035
    draw.line([(450, out_y2), (450, merge6_y), (2050, merge6_y), (2050, out_y2)], fill="#334155", width=5)
    draw.line([(cx, out_y2), (cx, merge6_y)], fill="#334155", width=5)
    draw_arrow_down(draw, cx, merge6_y, 3100, color="#334155", width=5)

    # STEP 6: OUTPUT PILL
    s6_box = (320, 3100, 2180, 3230)
    draw.rounded_rectangle(s6_box, radius=65, fill="#059669", outline="#047857", width=4)
    t6 = "6. XUẤT KẾT QUẢ TỪNG CÂU ĐỘC LẬP & CẬP NHẬT ONTOLOGY (v-idiomV6.rdf)"
    b6 = draw.textbbox((0, 0), t6, font=f_s1_t)
    draw.text((cx - (b6[2] - b6[0]) / 2, 3147), t6, font=f_s1_t, fill="#ffffff")

    out_paths = [
        Path("/Users/phandangvu/Desktop/ontology/onto-python/labse_pipeline/diagrams/labse_hybrid_flowchart.png"),
        Path("/Users/phandangvu/Desktop/ontology/onto-python/v_idiom_clean_flowchart.png"),
        Path("/Users/phandangvu/.gemini/antigravity-cli/brain/9dcd8af7-79bb-4f65-9322-a0886c4b9b51/labse_hybrid_flowchart.png"),
    ]
    for p in out_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        img.save(p, format="PNG")
        print("Saved:", p)


if __name__ == "__main__":
    main()
