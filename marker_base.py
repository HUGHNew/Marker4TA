from typing import Callable, Optional
from dataclasses import dataclass
import sys
import os.path as osp
import math

# pip install pypdf reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

# region font preset
# You can download the font from https://github.com/notofonts/noto-cjk
LocalSCFontPath = "assets/NotoSerifSC-VF.ttf"
AbsSCFontPath = osp.join(osp.dirname(sys.argv[0]), LocalSCFontPath)
SCFontName = "NotoSC"
pdfmetrics.registerFont(TTFont(SCFontName, AbsSCFontPath))


@dataclass
class FontInfo:
    name: str
    size: float
    color: colors.Color


def get_default_zh_font(scaler: int) -> FontInfo:
    return FontInfo(SCFontName, 16 * scaler, colors.lightblue)


def get_default_en_font(scaler: int) -> FontInfo:
    return FontInfo("Times-Roman", 28 * scaler, colors.red)


# endregion font preset

# DefaultPageWidth, DefaultPageHeight = 595.3, 841.9
DefaultPageSize = 595.3 * 841.9


def get_page_size(src: str) -> tuple[float, float]:
    reader = PdfReader(src)
    assert len(reader.pages) > 0, "Empty PDF provided"
    page = reader.pages[0]
    _, _, w, h = page.mediabox

    return (w, h)


def get_text_size(text: str, fontname, fontsize) -> tuple[float, float]:
    """
    :return: (width, height) in float
    """
    w = pdfmetrics.stringWidth(text, fontname, fontsize)
    asc, dsc = pdfmetrics.getAscentDescent(fontname, fontsize)
    h = asc - dsc
    return (w, h)


def create_sign_pdf(
    pdfname: str,
    content: str,
    pagesize: tuple[float, float] | str,
    extra: Optional[str] = None,
    xstart: float = 10,
    loff=5,
    font_primary: Optional[FontInfo] = None,
    font_secondary: Optional[FontInfo] = None,
):
    """
    Create a signed pdf with content and outilier rectangle.
    Args:
        pdfname: str, output pdf file name
        content: str, content to be signed
        xstart: float, x coordinate of the start of the content, default is 10. The origin is at the top left corner of the page. (Different from the origin of the coordinate system in math which is the standard view of reportlab.)
        loff: float, coordinate offset for rect, default is 5.
        font_primary: FontInfo, primary font info for score, default is Times-Roman 28*scaler red.
        font_secondary: FontInfo, secondary font info for extra reasons, default is NotoSC 16*scaler lightblue.
    """
    if isinstance(pagesize, str):
        width, height = get_page_size(pagesize)
    elif isinstance(pagesize, tuple):
        assert len(pagesize) == 2, "pagesize should be a tuple of (width, height)"
        width, height = pagesize
    else:
        raise TypeError("pagesize should be a str or a tuple of (width, height)")

    scaler = math.ceil((abs(width * height - DefaultPageSize) + 1e-6) / DefaultPageSize)
    font_primary = font_primary if font_primary else get_default_en_font(scaler)
    font_secondary = font_secondary if font_secondary else get_default_zh_font(scaler)

    c = canvas.Canvas(pdfname, pagesize=(width, height))

    # draw score text
    c.setFillColor(font_primary.color)
    c.setFont(font_primary.name, font_primary.size)
    tw, th = get_text_size(content, font_primary.name, font_primary.size)
    x, y = xstart, th + loff
    c.drawString(x, height - y, content)

    # draw score frame
    c.setStrokeColor(font_primary.color)
    c.rect(x - loff, height - y - loff, tw + 2 * loff, th + 2 * loff)

    if extra is not None:
        # draw extra text if provided
        c.setFillColor(font_secondary.color)
        c.setFont(font_secondary.name, font_secondary.size)
        ex, ey = x + tw + 2 * loff, th

        width_limit = width - ex
        extra_lines = extra.split("\n")
        max_line_width = max(
            (get_text_size(line, font_secondary.name, font_secondary.size)[0] for line in extra_lines)
        )
        line_height = get_text_size(extra, font_secondary.name, font_secondary.size)[1] + loff
        if max_line_width > width_limit:
            # resize for line fit
            fit_size = font_secondary.size * (width_limit - loff) / max_line_width
            c.setFontSize(fit_size)
        for line in extra_lines:
            c.drawString(ex, height - ey, line)
            ey += line_height

    c.showPage()
    c.save()


def mark_task(
    src_pdf: str,
    content: str,
    sign_pdf: str,
    out_pdf: str,
    extra: Optional[str] = None,
    signer: Callable[
        [str, str, tuple[float, float] | str, Optional[str]], None
    ] = create_sign_pdf,
):
    """
    Args:
        src_pdf: str, input pdf file name
        content: str, content to be signed
        sign_pdf: str, output pdf file name for the signature (temporary file)
        out_pdf: str, output pdf file name for the marked task
    """
    signer(sign_pdf, content, src_pdf, extra)
    src = PdfReader(src_pdf)
    sign = PdfReader(sign_pdf)
    pages = src.pages
    pages[0].merge_page(sign.pages[0])
    out = PdfWriter()
    for p in pages:
        out.add_page(p)
    out.write(out_pdf)
    out.close()
