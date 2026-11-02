import csv
import os
import re
from pathlib import Path
from owlready2 import (
    get_ontology,
    Thing,
    ObjectProperty,
    PropertyChain,
    locstr,
    World,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CSV_V5_PATH = ROOT_DIR / "200_idioms-v5.csv"
MD_V5_PATH = ROOT_DIR / "Bể_tiêu_chí-v5.md"
OUTPUT_RDF_PATH = ROOT_DIR / "ontology_protege" / "v-idiomV6.rdf"

BASE_IRI = "http://www.semanticweb.org/phandangvu/ontologies/2026/8/v-idiomv2#"


def sanitize_iri_name(name: str) -> str:
    """Chuẩn hóa tên thành ngữ thành định danh IRI hợp lệ trong XML/RDF (giống chuẩn v5)."""
    s = str(name or "").strip()
    for ch in [",", "'", "’", "?", "!", '"', ";", ":"]:
        s = s.replace(ch, "")
    return "_".join(s.split())


def parse_criteria_from_markdown(md_path: Path) -> dict[str, dict[str, str]]:
    """Đọc toàn bộ 236 mã tiêu chí và định nghĩa từ Bể_tiêu_chí-v5.md."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    pattern = re.compile(
        r"^\|\s*`((?:BC|MD|HD|KQ)_[^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(\d+)\s*\|",
        re.MULTILINE,
    )
    criteria = {}
    for code, desc_vi, ctype, examples, count in pattern.findall(md_text):
        code = code.strip()
        criteria[code] = {
            "code": code,
            "prefix": code.split("_", 1)[0],
            "desc_vi": desc_vi.strip(),
            "type": ctype.strip(),
            "examples": examples.strip(),
            "count": int(count),
        }
    return criteria


def build_v6_ontology():
    criteria_dict = parse_criteria_from_markdown(MD_V5_PATH)
    print(f"✅ Đã đọc {len(criteria_dict)} mã tiêu chí từ {MD_V5_PATH.name}")

    with open(CSV_V5_PATH, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"✅ Đã đọc {len(rows)} cặp thành ngữ từ {CSV_V5_PATH.name}")

    world = World()
    onto = world.get_ontology(BASE_IRI)

    with onto:
        # --- Định nghĩa các Lớp (Classes) ---
        class Thành_ngữ_Tục_ngữ(Thing):
            pass

        class Vietnamese_idiom(Thành_ngữ_Tục_ngữ):
            pass

        class English_Idiom(Thành_ngữ_Tục_ngữ):
            pass

        class Tiêu_chí(Thing):
            pass

        class Bối_cảnh(Tiêu_chí):
            pass

        class Hành_động(Tiêu_chí):
            pass

        class Kết_quả(Tiêu_chí):
            pass

        class Mục_đích(Tiêu_chí):
            pass

        class Khung_Bản_Thể_học(Thing):
            pass

        # --- Định nghĩa các Thuộc tính (Object Properties) ---
        class Có_bối_cảnh(ObjectProperty):
            domain = [Khung_Bản_Thể_học]
            range = [Bối_cảnh]

        class Có_hành_động(ObjectProperty):
            domain = [Khung_Bản_Thể_học]
            range = [Hành_động]

        class Có_kết_quả(ObjectProperty):
            domain = [Khung_Bản_Thể_học]
            range = [Kết_quả]

        class Có_mục_đích(ObjectProperty):
            domain = [Khung_Bản_Thể_học]
            range = [Mục_đích]

        # Quan hệ 2 chiều giữa Thành_ngữ_Tục_ngữ và Khung_Bản_Thể_học
        class Là_khung_của(ObjectProperty):
            domain = [Khung_Bản_Thể_học]
            range = [Thành_ngữ_Tục_ngữ]

        class Có_khung(ObjectProperty):
            domain = [Thành_ngữ_Tục_ngữ]
            range = [Khung_Bản_Thể_học]
            inverse_property = Là_khung_của

        # Luật Bắc cầu (Property Chain Axiom): Có_khung o Là_khung_của -> Có_nghĩa
        class Có_nghĩa(ObjectProperty):
            domain = [Thành_ngữ_Tục_ngữ]
            range = [Thành_ngữ_Tục_ngữ]
            property_chain = [PropertyChain([Có_khung, Là_khung_của])]

        # --- 1. Khởi tạo các cá thể Tiêu chí (236 mã) kèm rdfs:comment ---
        cls_map = {
            "BC": Bối_cảnh,
            "HD": Hành_động,
            "KQ": Kết_quả,
            "MD": Mục_đích,
        }
        criteria_instances = {}
        for code, info in criteria_dict.items():
            target_cls = cls_map[info["prefix"]]
            inst = target_cls(code)
            inst.comment = [info["desc_vi"]]
            criteria_instances[code] = inst

        # Đảm bảo mọi mã trong CSV đều có cá thể
        for r in rows:
            for col, prefix in [
                ("Bối cảnh", "BC"),
                ("Mục đích", "MD"),
                ("Hành động", "HD"),
                ("Kết quả", "KQ"),
            ]:
                val = (r.get(col) or "").strip()
                if val and val not in criteria_instances:
                    inst = cls_map[prefix](val)
                    criteria_instances[val] = inst

        # --- 2. Khởi tạo Khung_Bản_Thể_học và 200 cặp Thành ngữ Việt - Anh ---
        frame_dict = {}
        vn_comment_count = 0
        en_comment_count = 0

        for r in rows:
            vn_raw = (r.get("Thành Ngữ Việt Nam") or "").strip()
            en_raw = (r.get("Thành ngữ Tiếng Anh") or "").strip()
            meaning_vn = (r.get("Giải nghĩa tiếng Việt") or "").strip()
            meaning_en = (r.get("giải nghĩa tiếng Anh") or "").strip()

            bc = (r.get("Bối cảnh") or "").strip()
            md = (r.get("Mục đích") or "").strip()
            hd = (r.get("Hành động") or "").strip()
            kq = (r.get("Kết quả") or "").strip()

            frame_key = f"{bc}|{hd}|{kq}|{md}"
            if frame_key not in frame_dict:
                frame_name = f"Khung{len(frame_dict) + 1}"
                new_frame = Khung_Bản_Thể_học(frame_name)
                if bc:
                    new_frame.Có_bối_cảnh.append(criteria_instances[bc])
                if hd:
                    new_frame.Có_hành_động.append(criteria_instances[hd])
                if kq:
                    new_frame.Có_kết_quả.append(criteria_instances[kq])
                if md:
                    new_frame.Có_mục_đích.append(criteria_instances[md])
                frame_dict[frame_key] = new_frame

            current_frame = frame_dict[frame_key]

            if vn_raw:
                vn_clean = sanitize_iri_name(vn_raw)
                vn_inst = Vietnamese_idiom(vn_clean)
                if current_frame not in vn_inst.Có_khung:
                    vn_inst.Có_khung.append(current_frame)
                if meaning_vn:
                    vn_inst.comment = [locstr(meaning_vn, lang="vi")]
                    vn_comment_count += 1

            if en_raw:
                en_clean = sanitize_iri_name(en_raw)
                en_inst = English_Idiom(en_clean)
                if current_frame not in en_inst.Có_khung:
                    en_inst.Có_khung.append(current_frame)
                if meaning_en and not en_inst.comment:
                    en_inst.comment = [locstr(meaning_en, lang="en")]
                    en_comment_count += 1

    OUTPUT_RDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    onto.save(file=str(OUTPUT_RDF_PATH), format="rdfxml")

    print(f"🎉 Đã lưu thành công Ontology v6 tại: {OUTPUT_RDF_PATH}")
    print(f"   - Tổng số Tiêu chí (Tiêu_chí): {len(onto.Tiêu_chí.instances())} (BC: {len(onto.Bối_cảnh.instances())}, MD: {len(onto.Mục_đích.instances())}, HD: {len(onto.Hành_động.instances())}, KQ: {len(onto.Kết_quả.instances())})")
    print(f"   - Tổng số Khung Bản thể học (Khung_Bản_Thể_học): {len(frame_dict)}")
    print(f"   - Tổng số Thành ngữ Tiếng Việt (Vietnamese_idiom): {len(onto.Vietnamese_idiom.instances())} (đã gán {vn_comment_count} comment @vi)")
    print(f"   - Tổng số Thành ngữ Tiếng Anh (English_Idiom): {len(onto.English_Idiom.instances())} (đã gán {en_comment_count} comment @en)")


if __name__ == "__main__":
    build_v6_ontology()
