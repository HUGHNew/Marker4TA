"""convert UTF-8 csv to UTF-8-BOM csv
"""

import fire


def with_BOM(source: str, target: str, header: str = "", src_encoding="utf-8"):
    """
    Args:
        source: the path of the source file
        target: the path of the target file
        header: Optional mappered header for the original csv file (DOT sperated for fire parse)
        src_encoding: Optional encoding of the source file, default is "utf-8"
    """
    with open(source, encoding=src_encoding) as reader:
        content = reader.readlines()
    with open(target, "w", encoding="utf-8-sig") as writer:
        if header:
            header = header.replace(".", ",")
            writer.write(header)
            writer.write("\n")
            content = content[1:]
        writer.writelines(content)


if __name__ == "__main__":
    fire.Fire(with_BOM, name="bomer")
