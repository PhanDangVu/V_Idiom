import re

md_path = 'be_tieu_chi_chung_cap_nhat_v3.md'
criteria_meanings = {}

with open(md_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Tự viết regex đơn giản hơn để bắt tất cả các trường hợp
        # Ví dụ dòng: | **BC_Giao_tiếp**          | Tình huống nói chuyện, đàm phán, phô trương ý kiến. | Gốc        |
        # Hoặc dòng:  | **BC\_*Gia*đình**        | Quan hệ huyết thống, gia tộc, cha con, anh em.           | Mới v2     |
        parts = line.split('|')
        if len(parts) >= 4:
            col1 = parts[1].strip()
            col2 = parts[2].strip()
            if col1.startswith('**') and col1.endswith('**'):
                raw_name = col1.replace('**', '').replace('\\', '').replace('*', '').strip()
                criteria_meanings[raw_name] = col2
                print(f"Matched: {raw_name} -> {col2}")

print(f"Tổng cộng: {len(criteria_meanings)}")
