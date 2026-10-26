# -*- coding: utf-8 -*-
"""moddoc — Sinh văn bản Word theo bố cục hành chính Bộ Quốc phòng
(Nghị định 30/2020/NĐ-CP, Phụ lục I + Thông tư 52/2021/TT-BQP).

Yêu cầu: python-docx (cài trong venv riêng, KHÔNG dùng --break-system-packages).
    python3 -m venv .docvenv && .docvenv/bin/pip install python-docx

Dùng nhanh (có trang bìa + mục lục):
    from moddoc import MoDDoc
    d = MoDDoc(co_quan_tren="QUÂN CHỦNG X", don_vi="CỤC Y",
              ten_loai="TÀI LIỆU HƯỚNG DẪN SỬ DỤNG",
              trich_yeu="Hệ thống ...", img_dir="docs/images",
              build_front=False)              # tự dựng front matter theo ý
    d.cover(dia_danh="Hà Nội", nam="2026")    # trang bìa (trang 1)
    d.toc()                                     # mục lục (field, tự cập nhật)
    d.header_block(); d.title_block()           # Quốc hiệu + tên loại (đầu nội dung)
    d.h1("I", "Quy định chung")
    d.h2("1", "Mục đích")
    d.para("Nội dung ...", indent=True)
    d.step(1, [("Nhấn nút ", {}), ("Lưu", {"bold": True}), (". Chờ báo thành công.", {})])
    d.box("CHÚ Ý:", [("Không chia sẻ tài khoản.", {})])
    d.image("hinh1.jpg", "Màn hình đăng nhập.")
    d.table(["Cột A", "Cột B"], [["1", "2"]])
    d.signature()          # khối ký (tùy chọn)
    d.save("docs/TAI_LIEU.docx")

Cách gọi tối giản (giữ tương thích cũ, KHÔNG bìa/mục lục):
    d = MoDDoc(...)        # tự dựng Quốc hiệu + tên loại ngay đầu văn bản

Chuẩn áp dụng (NĐ 30/2020, Phụ lục I):
- Khổ A4; lề trên/dưới 20mm, trái 30mm, phải 15mm.
- Phông Times New Roman; nội dung cỡ 14, bảng/chú thích 13; dãn dòng 1.5;
  đoạn cách nhau 6pt; lùi đầu dòng 1cm.
- Quốc hiệu (in hoa, cỡ 13, đậm) – Tiêu ngữ (cỡ 14, đậm, có đường kẻ dưới) ở góc phải;
  tên cơ quan chủ quản (cỡ 13) + đơn vị ban hành (cỡ 13, đậm, đường kẻ dưới) ở góc trái.
- Tên loại (in hoa, đậm, căn giữa) + trích yếu (đậm, căn giữa, đường kẻ dưới 1/3–1/2 dòng).
- SỐ TRANG: chữ số Ả Rập, cỡ 13–14, canh giữa theo chiều ngang trong phần LỀ TRÊN
  (header), KHÔNG hiển thị ở trang thứ nhất.
"""
import os
from docx import Document
from docx.shared import Pt, Mm, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
BODY = 14
# Thông tư 22/2021/TT-BQP (PDF hướng dẫn tr.2): "chữ đầu dòng lùi vào 1,27cm (1 tab)"
LUI_DAU_DONG_CM = 1.27
# Ngoài phạm vi TT22 — quy ước dùng chung cho mọi tài liệu của cả hai dự án,
# để bản sinh bằng pandoc và bản sinh bằng python-docx trông giống nhau.
NEN_HOP = "F2F2F2"            # nền hộp CHÚ Ý / LƯU Ý QUAN TRỌNG
NEN_TIEU_DE_BANG = "D9D9D9"   # nền dòng tiêu đề của bảng
CENTER = WD_ALIGN_PARAGRAPH.CENTER


class MoDDoc:
    def __init__(self, co_quan_tren="[TÊN CƠ QUAN CHỦ QUẢN]", don_vi="[TÊN ĐƠN VỊ BAN HÀNH]",
                 ten_loai="TÀI LIỆU", trich_yeu="", ghi_chu_ban_hanh="", img_dir=".",
                 build_front=True, so_trang="top"):
        """so_trang: 'top' = số trang ở lề trên, canh giữa (đúng NĐ 30/2020);
        'bottom' = chân trang (một số đơn vị quen dùng cho tài liệu nhiều trang)."""
        self.img_dir = img_dir
        self._fig = 0
        self.co_quan_tren = co_quan_tren
        self.don_vi = don_vi
        self.ten_loai = ten_loai
        self.trich_yeu = trich_yeu
        self.ghi_chu_ban_hanh = ghi_chu_ban_hanh
        self.doc = Document()
        self._setup_page()
        self._setup_normal()
        self._page_numbers(so_trang)
        self._enable_update_fields()
        if build_front:
            self.header_block()
            self.title_block()

    # ---------- thiết lập ----------
    def _setup_page(self):
        s = self.doc.sections[0]
        s.page_width, s.page_height = Mm(210), Mm(297)
        s.top_margin, s.bottom_margin = Mm(20), Mm(20)
        s.left_margin, s.right_margin = Mm(30), Mm(15)
        # số trang nằm trong lề trên -> chừa khoảng header
        s.header_distance, s.footer_distance = Mm(10), Mm(10)
        s.different_first_page_header_footer = True
        self.sec = s

    def _setup_normal(self):
        n = self.doc.styles["Normal"]
        n.font.name = FONT; n.font.size = Pt(BODY)
        n.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        n.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        n.paragraph_format.line_spacing = 1.5
        n.paragraph_format.space_after = Pt(0)
        # Căn đều hai biên: NĐ 30/2020 không quy định bắt buộc, nhưng là quy ước
        # trình bày của văn bản hành chính. Các đoạn căn giữa (Quốc hiệu, tên loại,
        # chú thích hình) tự đặt CENTER nên không bị ảnh hưởng.
        n.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def _enable_update_fields(self):
        """Buộc Word cập nhật toàn bộ field (mục lục, số trang) khi mở file."""
        settings = self.doc.settings.element
        uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
        settings.append(uf)

    # ---------- tiện ích low-level ----------
    def _run(self, r, size=BODY, bold=False, italic=False, caps=False, color=None):
        r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        rpr = r._element.get_or_add_rPr(); rpr.rFonts.set(qn("w:eastAsia"), FONT)
        if caps:
            e = OxmlElement("w:caps"); e.set(qn("w:val"), "true"); rpr.append(e)
        if color:
            r.font.color.rgb = color

    def _no_borders(self, table):
        pr = table._tbl.tblPr; b = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "none"); b.append(e)
        pr.append(b)

    def _fixed_layout(self, table, widths):
        """Cố định độ rộng cột (chống co giãn/xuống dòng ngoài ý muốn)."""
        table.autofit = False
        table.allow_autofit = False
        pr = table._tbl.tblPr
        lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); pr.append(lay)
        for i, w in enumerate(widths):
            for row in table.rows:
                row.cells[i].width = w
            table.columns[i].width = w

    def _bottom_border(self, p):
        pPr = p._p.get_or_add_pPr(); bd = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "8"); bt.set(qn("w:space"), "1")
        bt.set(qn("w:color"), "000000"); bd.append(bt); pPr.append(bd)

    def _shade(self, cell, hexfill):
        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto")
        sh.set(qn("w:fill"), hexfill); cell._tc.get_or_add_tcPr().append(sh)

    def _tight_cells(self, table, margin_tw=0):
        """Ép lề trong ô về 0 (dùng cho bảng tiêu đề để chuỗi dài không bị xuống dòng)."""
        pr = table._tbl.tblPr; cm = OxmlElement("w:tblCellMar")
        for edge in ("top", "left", "bottom", "right"):
            e = OxmlElement(f"w:{edge}"); e.set(qn("w:w"), str(margin_tw))
            e.set(qn("w:type"), "dxa"); cm.append(e)
        pr.append(cm)

    def _outline(self, p, level):
        """Đánh outline level để field MỤC LỤC bắt được (giữ nguyên định dạng TNR)."""
        pPr = p._p.get_or_add_pPr(); o = OxmlElement("w:outlineLvl")
        o.set(qn("w:val"), str(level)); pPr.append(o)

    # ---------- trang bìa ----------
    def cover(self, dia_danh="", nam="", logo=None, ban_hanh_kem=""):
        """Trang bìa (trang 1): cơ quan trên/đơn vị ở đầu, tên tài liệu ở giữa,
        địa danh – năm ở cuối. Kết thúc bằng ngắt trang."""
        self.para(self.co_quan_tren, size=14, bold=True, caps=True, align=CENTER, before=6, after=0)
        self.para(self.don_vi, size=14, bold=True, caps=True, align=CENTER, after=0)
        line = self.para("", after=0); self._bottom_border(line)
        line.paragraph_format.left_indent = Cm(5.5); line.paragraph_format.right_indent = Cm(5.5)
        if logo:
            p = self.doc.add_paragraph(); p.alignment = CENTER
            p.paragraph_format.space_before = Pt(48); p.paragraph_format.space_after = Pt(0)
            p.add_run().add_picture(os.path.join(self.img_dir, logo), width=Cm(4))
            self.para("", before=24, after=0)
        else:
            self.para("", before=90, after=0)
        self.para(self.ten_loai, size=22, bold=True, caps=True, align=CENTER, after=6)
        if self.trich_yeu:
            self.para(self.trich_yeu, size=16, bold=True, align=CENTER, after=6)
        if ban_hanh_kem:
            self.para(ban_hanh_kem, size=13, italic=True, align=CENTER, after=6)
        self.para("", before=170, after=0)
        if dia_danh or nam:
            txt = f"{dia_danh}, năm {nam}" if (dia_danh and nam) else (dia_danh or f"Năm {nam}")
            self.para(txt, size=14, bold=True, italic=True, align=CENTER, after=0)
        self.page_break()

    # ---------- mục lục ----------
    def toc(self, tieu_de="MỤC LỤC", levels="1-3"):
        """Chèn field MỤC LỤC (tự cập nhật số trang khi mở trong Word do đã bật
        updateFields). Kết thúc bằng ngắt trang."""
        self.para(tieu_de, bold=True, caps=True, align=CENTER, before=6, after=10)
        p = self.doc.add_paragraph()
        r = p.add_run(); self._run(r)
        f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
        it.text = f' TOC \\o "{levels}" \\h \\z \\u '
        f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
        t = OxmlElement("w:t"); t.text = "Nhấn chuột phải vào đây → Update Field để hiện mục lục."
        f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
        r._r.append(f1); r._r.append(it); r._r.append(f2); r._r.append(t); r._r.append(f3)
        self.page_break()

    def page_break(self):
        p = self.doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)

    # ---------- khối đầu văn bản ----------
    def header_block(self):
        t = self.doc.add_table(rows=1, cols=2)
        # cột phải rộng + lề ô = 0 để Quốc hiệu (≈9,5cm ở cỡ 13) KHÔNG bị xuống dòng
        self._fixed_layout(t, [Cm(6.0), Cm(10.5)])
        self._tight_cells(t)
        lc, rc = t.cell(0, 0), t.cell(0, 1)
        p = lc.paragraphs[0]; p.alignment = CENTER; p.paragraph_format.space_after = Pt(0)
        self._run(p.add_run(self.co_quan_tren), size=13, caps=True)
        p2 = lc.add_paragraph(); p2.alignment = CENTER; p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.left_indent = Cm(1.0); p2.paragraph_format.right_indent = Cm(1.0)
        self._run(p2.add_run(self.don_vi), size=13, bold=True, caps=True); self._bottom_border(p2)
        q = rc.paragraphs[0]; q.alignment = CENTER; q.paragraph_format.space_after = Pt(0)
        self._run(q.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"), size=13, bold=True)
        q2 = rc.add_paragraph(); q2.alignment = CENTER; q2.paragraph_format.space_after = Pt(0)
        q2.paragraph_format.left_indent = Cm(2.0); q2.paragraph_format.right_indent = Cm(2.0)
        self._run(q2.add_run("Độc lập - Tự do - Hạnh phúc"), size=14, bold=True); self._bottom_border(q2)
        self._no_borders(t)

    def title_block(self):
        self.para("", after=6)
        self.para(self.ten_loai, bold=True, caps=True, align=CENTER, after=0)
        if self.trich_yeu:
            p = self.para(self.trich_yeu, bold=True, align=CENTER, after=2)
            # đường kẻ ngang dưới trích yếu, dài ~1/3–1/2 dòng, căn giữa
            p.paragraph_format.left_indent = Cm(4.5); p.paragraph_format.right_indent = Cm(4.5)
            self._bottom_border(p)
        if self.ghi_chu_ban_hanh:
            self.para(self.ghi_chu_ban_hanh, size=13, italic=True, align=CENTER, before=4, after=12)
        else:
            self.para("", after=8)

    def _page_numbers(self, pos="top"):
        """NĐ 30/2020: số trang canh giữa trong lề trên; không hiện ở trang 1."""
        container = self.sec.header if pos == "top" else self.sec.footer
        p = container.paragraphs[0]; p.alignment = CENTER
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(0)
        r = p.add_run(); self._run(r, size=BODY)
        a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"), "begin")
        i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = "PAGE"
        z = OxmlElement("w:fldChar"); z.set(qn("w:fldCharType"), "end")
        r._r.append(a); r._r.append(i); r._r.append(z)

    # ---------- API nội dung ----------
    def para(self, text="", size=BODY, bold=False, italic=False, align=None,
             before=0, after=6, indent=False, caps=False):
        p = self.doc.add_paragraph()
        if align is not None: p.alignment = align
        p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
        if indent: p.paragraph_format.first_line_indent = Cm(LUI_DAU_DONG_CM)
        if text:
            self._run(p.add_run(text), size=size, bold=bold, italic=italic, caps=caps)
        return p

    def runs(self, parts, before=0, after=6, indent=False):
        """parts: list[(text, {bold/italic/...})] — in đậm cụm tên giao diện trong 1 đoạn."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
        if indent: p.paragraph_format.first_line_indent = Cm(LUI_DAU_DONG_CM)
        for t, kw in parts:
            self._run(p.add_run(t), **kw)
        return p

    def h1(self, num, text):
        p = self.doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6); p.paragraph_format.keep_with_next = True
        self._run(p.add_run(f"{num}. {text}"), bold=True, caps=True)
        self._outline(p, 0)

    def h2(self, num, text):
        p = self.doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True
        self._run(p.add_run(f"{num}. {text}"))
        self._outline(p, 1)

    def h3(self, text):
        p = self.doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
        self._run(p.add_run(text), bold=True, italic=True)
        self._outline(p, 2)

    def step(self, n, parts):
        p = self.doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Cm(0.5)
        self._run(p.add_run(f"Bước {n}: "), bold=True)
        for t, kw in parts:
            self._run(p.add_run(t), **kw)

    def bullet(self, parts):
        p = self.doc.add_paragraph(); p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(3)
        self._run(p.add_run("- "))
        for t, kw in parts:
            self._run(p.add_run(t), **kw)

    def box(self, label, parts, fill=NEN_HOP):
        """Hộp cảnh báo. label = 'CHÚ Ý:' hoặc 'LƯU Ý QUAN TRỌNG:'. fill: FDECEA (đỏ nhạt) / FFF4CE (vàng)."""
        t = self.doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.style = "Table Grid"
        c = t.cell(0, 0); self._shade(c, fill)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.3
        self._run(p.add_run(label + " "), bold=True)
        for t2, kw in parts:
            self._run(p.add_run(t2), **kw)
        self.para("", after=2)

    def image(self, fname, caption, width_cm=15.5):
        self._fig += 1
        p = self.doc.add_paragraph(); p.alignment = CENTER
        p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(os.path.join(self.img_dir, fname), width=Cm(width_cm))
        cap = self.doc.add_paragraph(); cap.alignment = CENTER; cap.paragraph_format.space_after = Pt(8)
        self._run(cap.add_run(f"Hình {self._fig}. {caption}"), size=13, italic=True)

    def table(self, headers, rows, widths=None):
        t = self.doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]; self._shade(c, NEN_TIEU_DE_BANG)
            pp = c.paragraphs[0]; pp.alignment = CENTER; pp.paragraph_format.space_after = Pt(0)
            self._run(pp.add_run(h), size=13, bold=True)
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                pp = cells[i].paragraphs[0]; pp.paragraph_format.space_after = Pt(0)
                pp.paragraph_format.line_spacing = 1.15
                self._run(pp.add_run(val), size=13)
        if widths:
            self._fixed_layout(t, widths)
        return t

    def signature(self, left=("NGƯỜI BIÊN SOẠN", "(Ký, ghi rõ họ tên)"),
                  right=("THỦ TRƯỞNG ĐƠN VỊ", "(Ký tên, đóng dấu)")):
        self.para("", before=10, after=0)
        t = self.doc.add_table(rows=1, cols=2)
        for cell, lines in ((t.cell(0, 0), left), (t.cell(0, 1), right)):
            p = cell.paragraphs[0]; p.alignment = CENTER; p.paragraph_format.space_after = Pt(0)
            self._run(p.add_run(lines[0]), bold=True)
            p2 = cell.add_paragraph(); p2.alignment = CENTER
            self._run(p2.add_run(lines[1]), size=13, italic=True)
        self._no_borders(t)

    def save(self, path):
        self.doc.save(path); return path
