from typing import Callable

# pip install pypdf reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from pypdf import PdfReader, PdfWriter


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
    location: tuple[float, float] = (50, 50),
    loff=5,
    color: colors.Color = colors.red,
    fontname: str = "Times-Roman",
    fontsize: float = 28,
):
    """
    Create a signed pdf with content and outilier rectangle.
    Args:
        pdfname: str, output pdf file name
        content: str, content to be signed
        location: tuple[float, float], (x, y) coordinates of the text location on the page, default is (50, 50). The origin is at the top left corner of the page. (Different from the origin of the coordinate system in math which is the standard view of reportlab.)
        loff: float, coordinate offset for rect, default is 5.
    """
    if isinstance(pagesize, str):
        width, height = get_page_size(pagesize)
    elif isinstance(pagesize, tuple):
        assert len(pagesize) == 2, "pagesize should be a tuple of (width, height)"
        width, height = pagesize
    else:
        raise TypeError("pagesize should be a str or a tuple of (width, height)")

    c = canvas.Canvas(pdfname, pagesize=(width, height))
    c.setFillColor(color)
    c.setFont(fontname, fontsize)
    tw, th = get_text_size(content, fontname, fontsize)
    x, y = location
    c.drawString(x, height - y, content)
    c.setStrokeColor(colors.red)
    c.rect(x - loff, height - y - loff, tw + 2 * loff, th + 2 * loff)
    c.showPage()
    c.save()


def mark_task(
    src_pdf: str,
    content: str,
    sign_pdf: str,
    out_pdf: str,
    signer: Callable[[str, str, tuple[float, float] | str], None] = create_sign_pdf,
):
    """
    Args:
        src_pdf: str, input pdf file name
        content: str, content to be signed
        sign_pdf: str, output pdf file name for the signature (temporary file)
        out_pdf: str, output pdf file name for the marked task
    """
    # create_sign_pdf(sign_pdf, content, src_pdf)
    signer(sign_pdf, content, src_pdf)
    src = PdfReader(src_pdf)
    sign = PdfReader(sign_pdf)
    pages = src.pages
    pages[0].merge_page(sign.pages[0])
    out = PdfWriter()
    for p in pages:
        out.add_page(p)
    out.write(out_pdf)
    out.close()
