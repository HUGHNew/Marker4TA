import os
import os.path as osp

import fire

from header import PREGRADE_HEADER


def pre_grade(path: str, grade: int = 100, output="deduction.csv"):
    # TODO: define it yourself
    allow_ext = ["pdf", "zip"]
    sub_seq = [str(i) for i in range(1, 7)]
    header = PREGRADE_HEADER

    deduct = open(osp.join(path, output), "w", encoding="utf-8-sig")
    deduct.write(header + "\n")
    for file in os.listdir(path):
        delta = 0
        if file.endswith("csv") or osp.isdir(osp.join(path, file)):
            continue
        name, ext = file.split(".", 1)
        parts = name.split("-")
        lp = len(parts)
        if lp == 4:
            continue
        elif lp != 3:
            print(f"{file} need to process manually")
            continue

        records = []
        FORMAT_ERROR = 3
        NAME_ERROR = 2

        if ext.lower() not in allow_ext:
            delta += FORMAT_ERROR  # match format
            records.append(f"文件格式不符合要求(-{FORMAT_ERROR})")
        if len(parts[-1]) != 1 or parts[-1][0] not in sub_seq:
            delta += NAME_ERROR  # match submission name
            records.append(f"文件命名不符合要求(-{NAME_ERROR})")
        os.rename(osp.join(path, file), osp.join(path, f"{name}-{grade-delta}.{ext}"))
        if records:
            deduct.write(f"{parts[0]},{parts[1]},{'，'.join(records)},{delta}\n")
    deduct.close()


if __name__ == "__main__":
    fire.Fire(pre_grade)
