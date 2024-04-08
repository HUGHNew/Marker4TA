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
        sid = n[sid_idx : sid_idx + LEN_ID]
        if n.count("-") == 3:
            ld = n.rindex("-")
            n = n[:ld]
        assert sid.isnumeric(), f"SID:{sid} should be numeric"
        return f"{sid},{ext},{n}"

    __dir_walker(path, output, SUBMIT_HEADER, proc)


def backup(path: str, provider: str = "provider.csv", backup: str = "submission.csv"):
    # the recorder is partial csv of backup file
    # but it remains until better solution is found
    submission_record(path, provider)
    submission_backup(path, backup)


# FIXME: some refactor needed before first use for 24spring-asm
if __name__ == "__main__":
    fire.Fire(
        {
            "grade": submission_grades,  # write grades to csv
            "backup": backup,  # backup submission file name before manually modification for batch process
        }
    )
