"""
Tiny .xlsx writer for EPAY lead magnets, standard library only (no openpyxl
on this Mac). Every formula cell also stores its computed value, so previews
show numbers; spreadsheet apps recalculate on open (fullCalcOnLoad).
"""
import zipfile
from xml.sax.saxutils import escape

# ---------- styles ----------
# cellXfs index -> meaning
S = dict(default=0, title=1, header=2, in_text=3, in_money=4, in_num=5, in_pct=6,
         f_money=7, f_pct=8, note=9, label=10, total=11, body=12, sub=13, f_num=14)
styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="3">
<numFmt numFmtId="164" formatCode="&quot;$&quot;#,##0.00;(&quot;$&quot;#,##0.00);&quot;-&quot;"/>
<numFmt numFmtId="165" formatCode="0.0%;(0.0%);&quot;-&quot;"/>
<numFmt numFmtId="166" formatCode="#,##0.00;(#,##0.00);&quot;-&quot;"/>
</numFmts>
<fonts count="7">
<font><sz val="10"/><color rgb="FF0A1520"/><name val="Arial"/></font>
<font><b/><sz val="16"/><color rgb="FF0E6FA0"/><name val="Arial"/></font>
<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Arial"/></font>
<font><sz val="10"/><color rgb="FF0000FF"/><name val="Arial"/></font>
<font><i/><sz val="9"/><color rgb="FF4A5F70"/><name val="Arial"/></font>
<font><b/><sz val="10"/><color rgb="FF0A1520"/><name val="Arial"/></font>
<font><b/><sz val="11"/><color rgb="FF0A1520"/><name val="Arial"/></font>
</fonts>
<fills count="4">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF0E6FA0"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFF6D5"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="3">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left style="thin"><color rgb="FFCBDCE7"/></left><right style="thin"><color rgb="FFCBDCE7"/></right><top style="thin"><color rgb="FFCBDCE7"/></top><bottom style="thin"><color rgb="FFCBDCE7"/></bottom><diagonal/></border>
<border><left/><right/><top style="medium"><color rgb="FF0E6FA0"/></top><bottom/><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="15">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="center"/></xf>
<xf numFmtId="0" fontId="3" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="164" fontId="3" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="166" fontId="3" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="165" fontId="3" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="0" fontId="5" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="164" fontId="6" fillId="0" borderId="2" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1"/>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="0" fontId="6" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="166" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''

def col(n):
    s = ""
    while n: n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s

class Sheet:
    def __init__(self, name, widths, freeze=None):
        self.name, self.widths, self.freeze = name, widths, freeze
        self.rows, self.merges, self.heights = {}, [], {}
    def set(self, ref, value=None, style=0, formula=None):
        c = "".join(ch for ch in ref if ch.isalpha()); r = int("".join(ch for ch in ref if ch.isdigit()))
        self.rows.setdefault(r, {})[c] = (value, style, formula)
    def xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
               '<sheetViews><sheetView workbookViewId="0" showGridLines="0">']
        if self.freeze:
            out.append(f'<pane ySplit="{self.freeze - 1}" topLeftCell="A{self.freeze}" activePane="bottomLeft" state="frozen"/>')
        out.append('</sheetView></sheetViews><sheetFormatPr defaultRowHeight="15"/><cols>')
        for i, w in enumerate(self.widths, 1):
            out.append(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>')
        out.append('</cols><sheetData>')
        order = lambda c: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(c)))
        for r in sorted(self.rows):
            ht = f' ht="{self.heights[r]}" customHeight="1"' if r in self.heights else ""
            out.append(f'<row r="{r}"{ht}>')
            for c in sorted(self.rows[r], key=order):
                v, s, f = self.rows[r][c]
                ref = f"{c}{r}"
                if f is not None:
                    vv = "" if v is None else f"<v>{v}</v>"
                    out.append(f'<c r="{ref}" s="{s}"><f>{escape(f)}</f>{vv}</c>')
                elif v is None:
                    out.append(f'<c r="{ref}" s="{s}"/>')
                elif isinstance(v, (int, float)):
                    out.append(f'<c r="{ref}" s="{s}"><v>{v}</v></c>')
                else:
                    out.append(f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(v)}</t></is></c>')
            out.append('</row>')
        out.append('</sheetData>')
        if self.merges:
            out.append(f'<mergeCells count="{len(self.merges)}">' + "".join(f'<mergeCell ref="{m}"/>' for m in self.merges) + '</mergeCells>')
        out.append('<pageMargins left="0.5" right="0.5" top="0.6" bottom="0.6" header="0.3" footer="0.3"/>')
        out.append('<pageSetup orientation="landscape" fitToWidth="1" fitToHeight="0"/></worksheet>')
        return "".join(out)

r2 = lambda x: round(x + 1e-12, 6)



def save(OUT, sheets, title="EPAY POS"):
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets) + 1))
          + '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<sheets>' + "".join(f'<sheet name="{escape(s.name)}" sheetId="{i}" r:id="rId{i}"/>' for i, s in enumerate(sheets, 1)) + '</sheets>'
          '<calcPr calcId="191029" fullCalcOnLoad="1"/></workbook>')
    wbrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
              + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sheets) + 1))
              + f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>' + escape(title) + '</dc:title><dc:creator>EPAY POS</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels); z.writestr("docProps/core.xml", core)
        z.writestr("xl/workbook.xml", wb); z.writestr("xl/_rels/workbook.xml.rels", wbrels); z.writestr("xl/styles.xml", styles)
        for i, s in enumerate(sheets, 1): z.writestr(f"xl/worksheets/sheet{i}.xml", s.xml())

