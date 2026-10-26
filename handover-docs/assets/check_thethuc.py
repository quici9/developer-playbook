#!/usr/bin/env python3
"""Kiểm tra thể thức trình bày của tệp .docx theo Thông tư số 22/2021/TT-BQP.

    python3 check_thethuc.py <tệp.docx> [<tệp2.docx> ...]

Mục đích: hai tài liệu sinh ra từ hai công cụ khác nhau (pandoc và python-docx)
vẫn phải cho ra cùng một thể thức. Bộ kiểm này là chỗ duy nhất phát biểu thể thức
đó bằng con số, và là thứ phát hiện lệch thay cho việc so bằng mắt.

CĂN CỨ TỪNG CHỈ TIÊU (ghi rõ để sau này tra lại được):

[TT22] Thông tư số 22/2021/TT-BQP — trích qua Công văn hướng dẫn số 3365/BV-VP
       ngày 7/2021 của Bệnh viện TWQĐ 108 (bản chụp, 40 trang):
  - Nội dung văn bản: chữ in thường, canh đều cả 2 lề, kiểu đứng, cỡ chữ 14;
    khi xuống dòng, chữ đầu dòng lùi vào 1,27 cm (1 tab); khoảng cách giữa các
    đoạn văn tối thiểu 6 pt; khoảng cách giữa các dòng tối thiểu là dòng đơn,
    tối đa là 1,5 lines.                                            (PDF tr. 2)
  - Số trang: đánh từ số 1, chữ số Ả Rập, cỡ chữ 14, kiểu đứng, canh giữa theo
    chiều ngang, cách mép trên trang giấy 01 cm trong phần lề trên, không hiển
    thị trang thứ nhất.                                             (PDF tr. 1)
  - Phông chữ Times New Roman.                                   (PDF tr. 8-11)
  - Bố cục "phần, mục, khoản, điểm": số thứ tự và tiêu đề của MỤC in hoa, cỡ 14,
    đứng, đậm; KHOẢN in thường, cỡ 14, đứng (không đậm); ĐIỂM in thường, cỡ 14,
    đứng.                                                          (PDF tr. 10)

[NĐ30] Nghị định số 30/2020/NĐ-CP, Phụ lục I — dùng cho khổ giấy và định lề
       trang, vì bản hướng dẫn TT22 nói trên KHÔNG nêu hai chỉ tiêu này:
  - Khổ A4; lề trên 20-25 mm, lề dưới 20-25 mm, lề trái 30-35 mm, lề phải 15-20 mm.

[QUY ƯỚC] Ngoài phạm vi hai văn bản trên — chọn một kiểu và áp cho mọi tài liệu:
  - Chú thích hình: "Hình N. ...", cỡ 13, nghiêng, canh giữa.
  - Chữ trong bảng: cỡ 13.
  - Hộp cảnh báo: khung viền, nền xám nhạt.
"""
import re
import sys
import zipfile

TW_PER_MM = 56.7

# ---- Ngưỡng của từng chỉ tiêu (nửa-điểm cho cỡ chữ, twip cho kích thước) ----
KHO_A4 = (11906, 16838)
LE_TREN = (20, 25)
LE_DUOI = (20, 25)
LE_TRAI = (30, 35)
LE_PHAI = (15, 20)
CO_CHU_NOI_DUNG = 28        # 14pt
CO_CHU_SO_TRANG = 28        # 14pt
CO_CHU_BANG = 26            # 13pt
LUI_DAU_DONG = 720          # 1,27 cm
GIAN_DONG_TOI_DA = 360      # 1,5 lines
CACH_DOAN_TOI_THIEU = 120   # 6 pt
HEADER_CACH_MEP = 567       # 1 cm


class Ket:
    def __init__(self):
        self.rows = []

    def add(self, ten, dat, thuc_te, can_cu):
        self.rows.append((ten, dat, thuc_te, can_cu))

    def ok(self):
        return all(r[1] for r in self.rows)


def _mm(tw):
    return round(int(tw) / TW_PER_MM)


def _co_chu_mac_dinh(sty):
    """Cỡ chữ mặc định: ưu tiên style Normal, sau đó docDefaults."""
    # pandoc và python-docx viết thuộc tính theo thứ tự khác nhau, nên không được
    # đòi w:styleId đứng ngay trước dấu '>'.
    m = re.search(r'<w:style\b[^>]*w:styleId="Normal"[^>]*>.*?</w:style>', sty, re.S)
    if m:
        s = re.search(r'<w:sz w:val="(\d+)"', m.group(0))
        if s:
            return s.group(1)
    m = re.search(r'<w:docDefaults>.*?</w:docDefaults>', sty, re.S)
    if m:
        s = re.search(r'<w:sz w:val="(\d+)"', m.group(0))
        if s:
            return s.group(1)
    return '0'


def _styles_dung(doc, sty):
    """Chỉ giữ định nghĩa của những style THỰC SỰ được dùng trong document.xml,
    cộng docDefaults và Normal. Mẫu của python-docx/pandoc kèm theo hàng chục
    style dựng sẵn không dùng đến (Macro Text dùng Courier, Body Text 2 giãn dòng
    2.0...); soi cả những style chết đó sẽ báo lỗi giả."""
    dung = set(re.findall(r'<w:pStyle w:val="([^"]+)"', doc))
    dung |= set(re.findall(r'<w:tblStyle w:val="([^"]+)"', doc))
    dung |= {'Normal'}
    giu = []
    m = re.search(r'<w:docDefaults>.*?</w:docDefaults>', sty, re.S)
    if m:
        giu.append(m.group(0))
    for blk in re.findall(r'<w:style [^>]*>.*?</w:style>', sty, re.S):
        sid = re.search(r'w:styleId="([^"]+)"', blk)
        if sid and sid.group(1) in dung:
            giu.append(blk)
    return ''.join(giu)


def _attr(xml, pat, default=None):
    m = re.search(pat, xml)
    return m.group(1) if m else default


def kiem_tra(path):
    k = Ket()
    z = zipfile.ZipFile(path)
    doc = z.read('word/document.xml').decode()
    sty = z.read('word/styles.xml').decode()
    hdrs = [n for n in z.namelist() if re.match(r'word/header\d+\.xml', n)]
    hdr = z.read(hdrs[0]).decode() if hdrs else ''

    sect = re.search(r'<w:sectPr.*?</w:sectPr>', doc, re.S)
    sect = sect.group(0) if sect else ''

    # --- khổ giấy, lề ---
    w = _attr(sect, r'<w:pgSz[^>]*w:w="(\d+)"')
    h = _attr(sect, r'<w:pgSz[^>]*w:h="(\d+)"')
    k.add('Khổ giấy A4', (w, h) == (str(KHO_A4[0]), str(KHO_A4[1])),
          f'{_mm(w or 0)}x{_mm(h or 0)} mm', 'NĐ30 PL I')
    for ten, pat, rng in (('Lề trên', r'w:top="(\d+)"', LE_TREN),
                          ('Lề dưới', r'w:bottom="(\d+)"', LE_DUOI),
                          ('Lề trái', r'w:left="(\d+)"', LE_TRAI),
                          ('Lề phải', r'w:right="(\d+)"', LE_PHAI)):
        v = _attr(sect, r'<w:pgMar[^>]*' + pat)
        mm = _mm(v) if v else -1
        k.add(ten, rng[0] <= mm <= rng[1], f'{mm} mm', 'NĐ30 PL I')

    # --- phông chữ ---
    sty_dung = _styles_dung(doc, sty)
    fonts = set(re.findall(r'w:ascii="([^"]+)"', sty_dung)) | set(re.findall(r'w:ascii="([^"]+)"', doc))
    la = {f for f in fonts if f not in ('Times New Roman', 'Consolas', 'Courier New')}
    k.add('Phông Times New Roman', not la, ('có phông lạ: ' + ', '.join(sorted(la))) if la else 'đạt',
          'TT22 PL I')

    # --- cỡ chữ nội dung ---
    # Đo trên các đoạn VĂN XUÔI thật (ngoài bảng, dài >= 120 ký tự) để không vớ
    # phải cỡ chữ của trang bìa, đề mục hay mục lục.
    body = doc
    for t in re.findall(r'<w:tbl>.*?</w:tbl>', doc, re.S):
        body = body.replace(t, '')
    sizes = []
    for p_xml in re.findall(r'<w:p\b.*?</w:p>', body, re.S):
        txt = re.sub(r'<[^>]+>', '', p_xml)
        if len(txt) < 120 or 'PAGEREF' in p_xml:
            continue
        found = re.findall(r'<w:sz w:val="(\d+)"', p_xml)
        sizes.extend(found or [_co_chu_mac_dinh(sty)])
    pho_bien = max(set(sizes), key=sizes.count) if sizes else _co_chu_mac_dinh(sty)
    k.add('Cỡ chữ nội dung 14', pho_bien == str(CO_CHU_NOI_DUNG),
          f'{int(pho_bien)/2:g}pt', 'TT22 (PDF tr.2)')

    # --- căn đều hai biên ---
    k.add('Căn đều hai biên', 'w:jc w:val="both"' in sty or 'w:jc w:val="both"' in doc,
          'đạt' if ('w:jc w:val="both"' in sty or 'w:jc w:val="both"' in doc) else 'chưa đặt',
          'TT22 (PDF tr.2)')

    # --- lùi đầu dòng 1,27 cm ---
    inds = set(re.findall(r'w:firstLine="(\d+)"', doc)) | set(re.findall(r'w:firstLine="(\d+)"', sty_dung))
    inds = {i for i in inds if i != '0'}
    k.add('Lùi đầu dòng 1,27 cm', inds == {str(LUI_DAU_DONG)},
          ', '.join(f'{int(i)/TW_PER_MM*.1:.2f}cm' for i in sorted(inds)) or 'không có',
          'TT22 (PDF tr.2)')

    # --- giãn dòng tối đa 1,5 ---
    lines = [int(x) for x in re.findall(r'w:line="(\d+)"', doc) + re.findall(r'w:line="(\d+)"', sty_dung)]
    qua = sorted({x for x in lines if x > GIAN_DONG_TOI_DA})
    k.add('Giãn dòng ≤ 1,5', not qua, f'có dòng {qua}' if qua else 'đạt', 'TT22 (PDF tr.2)')

    # --- số trang ---
    co_page = 'PAGE' in hdr
    canh_giua = 'w:jc w:val="center"' in hdr
    # Mọi run trong header phải cùng cỡ 14 — nếu chỉ đòi "có một run cỡ 14" thì
    # đổi lẻ một run vẫn lọt (đã phát hiện bằng phép thử phá guard).
    co_hdr = set(re.findall(r'<w:sz w:val="(\d+)"', hdr))
    co_chu = bool(co_hdr) and co_hdr == {str(CO_CHU_SO_TRANG)}
    k.add('Số trang ở lề trên', co_page, 'đạt' if co_page else 'không có trường PAGE trong header',
          'TT22 (PDF tr.1)')
    k.add('Số trang canh giữa', canh_giua, 'đạt' if canh_giua else 'chưa canh giữa', 'TT22 (PDF tr.1)')
    k.add('Số trang cỡ 14', co_chu,
          ', '.join(f'{int(x)/2:g}pt' for x in sorted(co_hdr)) or 'không rõ',
          'TT22 (PDF tr.1)')
    hd = _attr(sect, r'w:header="(\d+)"')
    k.add('Số trang cách mép trên 1 cm', hd == str(HEADER_CACH_MEP),
          f'{int(hd)/TW_PER_MM:.0f} mm' if hd else 'không rõ', 'TT22 (PDF tr.1)')
    k.add('Không đánh số trang thứ nhất', '<w:titlePg' in sect,
          'đạt' if '<w:titlePg' in sect else 'thiếu titlePg', 'TT22 (PDF tr.1)')

    # --- bố cục đề mục ---
    lv = sorted(set(re.findall(r'<w:outlineLvl w:val="(\d)"', doc)))
    if not lv:  # pandoc dùng style Heading thay vì outlineLvl trực tiếp
        lv = sorted({m[-1] for m in re.findall(r'<w:pStyle w:val="(Heading\d)"', doc)})
        lv = [str(int(x) - 1) for x in lv]
    k.add('Đề mục không nhảy cấp', lv == [str(i) for i in range(len(lv))],
          'cấp ' + ', '.join(lv) if lv else 'không có đề mục', 'TT22 (PDF tr.10)')

    return k


def main(paths):
    tat_ca_dat = True
    ket_qua = {}
    for p in paths:
        k = kiem_tra(p)
        ket_qua[p] = k
        tat_ca_dat &= k.ok()
        print(f'\n=== {p} ===')
        w = max(len(r[0]) for r in k.rows)
        for ten, dat, tt, cc in k.rows:
            print(f'  [{"ĐẠT " if dat else "LỖI "}] {ten:<{w}}  {tt:<22} ({cc})')

    # so sánh chéo: mọi tệp phải cho cùng một kết quả trên từng chỉ tiêu
    if len(paths) > 1:
        print('\n=== ĐỐI CHIẾU GIỮA CÁC TÀI LIỆU ===')
        base = ket_qua[paths[0]]
        lech = 0
        for i, (ten, _, tt, _) in enumerate(base.rows):
            vals = {p: ket_qua[p].rows[i][2] for p in paths}
            if len(set(vals.values())) > 1:
                lech += 1
                print(f'  [LỆCH] {ten}')
                for p, v in vals.items():
                    print(f'           {p.split("/")[-1]}: {v}')
        if lech == 0:
            print(f'  {len(paths)} tài liệu trình bày giống hệt nhau trên mọi chỉ tiêu.')
        tat_ca_dat &= (lech == 0)

    return 0 if tat_ca_dat else 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
