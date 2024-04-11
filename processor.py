import os
import os.path as osp
from typing import Callable

import fire

from header import PROVIDER_HEADER, SCORE_HEADER, SUBMIT_HEADER


def __dir_walker(path: str, output: str, header: str, processor: Callable[[str], str]):
    """
    walk through the directory and process each file ignoring csv and directory
    Args:
        path: the directory to walk through
        output: the output file name
        header: the header of the output csv file
        processor: a function to process each file based filename
    """
    content = []
    for file in os.listdir(path):
        if file.endswith("csv") or osp.isdir(osp.join(path, file)):
            continue
        content.append(processor(file))
    with open(osp.join(path, output), "w", encoding="utf-8-sig") as fd:
        write_content = "\n".join(content)
        fd.write(f"{header}\n{write_content}")


def submission_record(path: str, output: str = "provider.csv"):
    # content = [ file.split('-')[1] for file in os.listdir(path) if not file.endswith("csv") ]
    def proc(name: str):
        parts = name.split("-")
        assert (
            len(parts) == 3 or len(parts) == 4
        ), f"{name}:{len(parts)} fatal format error"
        return parts[0] + "," + parts[1]

    __dir_walker(path, output, PROVIDER_HEADER, proc)


def submission_grades(path: str, output: str = "grades.csv"):
    """submission score writer"""

    def proc(name: str):
        n, _ = name.split(".")
        parts = n.split("-")
        assert len(parts) == 4, f"{name}:{len(parts)} fatal format error"
        return parts[0] + "," + parts[1] + "," + parts[3]

    __dir_walker(path, output, SCORE_HEADER, proc)


def submission_backup(path: str, output: str = "submission.csv"):
    def proc(name: str):
        LEN_ID = 13
        n, ext = name.split(".", 1)
        sid_idx = n.find("20")  # find it easilier to locate sid prefix
        # no match failure process here. All failed cases should be handled by submission_check
        sid = n[sid_idx : sid_idx + LEN_ID]
        if n.count("-") == 3:
            ld = n.rindex("-")
            n = n[:ld]
        assert sid.isnumeric(), f"SID:{sid} should be numeric"
        return f"{sid},{ext},{n}"

    __dir_walker(path, output, SUBMIT_HEADER, proc)


def backup(path: str, backup: str = "submission.csv"):
    # the recorder is partial csv of backup file
    # but it remains until better solution is found
    check_result = submission_check(path)
    if not check_result:
        print("Submission check failed, please make sure each submission comes with SID")
        return
    submission_backup(path, backup)
    # submission_record(path, provider)

def submission_check(path: str) -> bool:
    """check submission file name and format"""
    count, nosid = 0, 0
    for file in os.listdir(path):
        if file.endswith("csv"):
            continue
        part_count = file.count('-')
        if file.find("20") == -1:
            print(f"{file} does not contain SID")
            nosid += 1
            continue
        if part_count not in [3, 2]:
            print(f"{file} may use diff separator instead of '-'")
            count += 1
            continue
        _, ext = file.split(".", 1)
        if ext.lower() not in ["zip", "pdf", "ipynb"]:
            print(f"{file}:[{ext}] uses unexpected file extension")
            count += 1
            continue
    print(f"Total {count} errors found, {nosid} files without SID found")
    return nosid == 0

def submission_info_by_roster(sub: str, roster: str="names.csv"):
    with open(roster, "r", encoding="utf-8-sig") as fd:
        lines = fd.read().splitlines()[1:]
    rd, rl = {}, []
    for line in lines:
        seq, sid, name, _ = line.split(",", 3)
        rl.append(sid)
        rd[sid] = name
    nameset = set(rl)

    with open(sub, "r", encoding="utf-8-sig") as fd:
        lines = fd.read().splitlines()[1:]
    subset = set(line.split(",")[0] for line in lines)

    print(f"Total {len(subset)} submissions found, {len(nameset)} students in roster")

    nein = nameset - subset
    ja = subset - nameset

    for sid in nein:
        print(f"{rd[sid]} does not submit yet")

    for sid in ja:
        print(f"{sid} is unkown, but already submit")

if __name__ == "__main__":
    fire.Fire(
        {
            "grade": submission_grades,  # write grades to csv
            "backup": backup,  # backup submission file name before manually modification for batch process
            "check": submission_check,  # check submission file name and format
            "diff": submission_info_by_roster,  # check submission diff with roster
        }
    )
