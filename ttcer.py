"""
TTC font file extractor
"""
from fontTools.ttLib import TTCollection, TTFont
import os.path as osp

from fire import Fire
# TTC helper for extraction

def get_ttc_fonts_map(ttc_file:str) -> dict[str, TTFont]:
    """get font table from TTC file
    Args:
        ttc_file (str): TTC file path
    Returns:
        dict[str, TTFont]: font table. FullFontName: TTFont-object
    """
    ttc = TTCollection(ttc_file)
    return {font["name"].getDebugName(4): font for font in ttc.fonts}
# DebugName ref: https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids

def list_ttc_fonts(ttc_file:str):
    ttc_fonts = get_ttc_fonts_map(ttc_file)
    for idx, name in enumerate(ttc_fonts):
        print(f"{idx}: {name}")

def __extract_ttc_font_by_name(ttc:dict[str, TTFont], name:str, ttf:str):
    font = ttc.get(name)
    assert font is not None, f"Font {name} not found in TTC file"
    font.save(ttf)

def extract_ttc_font_by_name(ttc_file:str, name:str):
    ttc_fonts = get_ttc_fonts_map(ttc_file)
    ttf = osp.join(osp.dirname(ttc_file), name.replace(" ", "") + ".ttf")
    __extract_ttc_font_by_name(ttc_fonts, name, ttf)

def extract_ttc_font_by_index(ttc_file:str, index:int):
    ttc_fonts = get_ttc_fonts_map(ttc_file)
    assert index < len(ttc_fonts), f"Index {index}/{len(ttc_fonts)} out of range"
    font_name = list(ttc_fonts.keys())[index]
    ttf = osp.join(osp.dirname(ttc_file), font_name.replace(" ", "") + ".ttf")
    __extract_ttc_font_by_name(ttc_fonts, font_name, ttf)

if __name__ == '__main__':
    Fire({
        "list": list_ttc_fonts,
        "extract_idx": extract_ttc_font_by_index,
        "extract_name": extract_ttc_font_by_name,
    })