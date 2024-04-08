from functools import reduce
import os.path as osp

import fire

from header import STAT_HEADER

def get_submission_stats(
    path: str, reference: str
) -> tuple[dict[str, int], dict[str, str]]:
    ref = osp.join(path, reference)
    assert osp.exists(ref), f"file: {ref} doesn't exist. Generation grades file first"
    with open(ref, encoding="utf-8-sig") as r:
        content = r.readlines()[1:]
    grade_dict = {}  # sid:score
    sid_dict = {}  # sid:name
    for line in content:
        sid, name, score = line.strip().split(",")
        grade_dict[sid] = int(score)
        sid_dict[sid] = name
    return grade_dict, sid_dict


def submission_stats(path: str, reference: str = "grades.csv"):
    grade_dict, _ = get_submission_stats(path, reference)
    grades = list(grade_dict.values())
    print(f"avg: {sum(grades)/len(grades)}\tmin: {min(grades)}\tmax: {max(grades)}")


def get_roster_dict(file: str) -> dict[str, str]:
    with open(file, encoding="utf-8-sig") as reader:
        content = reader.readlines()[1:]
    roster = {}  # sid:name
    for line in content:
        sid, name = line.strip().split(",")
        roster[sid] = name
    return roster


def stringify_list(source: list, sep: str) -> str:
    return sep.join([str(it) for it in source])


def batch_stats(
    paths: list[str],
    weights: str = None,
    reference: str = "grades.csv",
    roster: str = "names.csv",
    storage: str = "billboard.csv",
):
    path_len = len(paths)
    if weights:
        weight_list = [int(p) for p in weights.split(",")]
        assert len(paths) == len(
            weight_list
        ), f"paths and weigths should have the same length"
    else:
        weight_list = [1] * path_len
    # weight norm
    weight_sum = sum(weight_list)
    weight_list = [w / weight_sum for w in weight_list]

    mapper = get_roster_dict(roster)
    grades = {sid: [] for sid in mapper}
    # data collection
    for p in paths:
        gd, _ = get_submission_stats(p, reference)
        # merge grades and mapper
        for sid in grades:
            grades[sid].append(gd.get(sid, 0))

    # write storage file
    header = STAT_HEADER.format(stringify_list(range(1, len(paths)+1), ',')) + '\n'
    with open(storage, "w", encoding="utf-8-sig") as writer:  # for xlsx recognization
        writer.write(header)
        for k, v in grades.items():
            mean = reduce(lambda acc, x: acc + x[0] * x[1], zip(v, weight_list), 0)
            writer.write(f"{k},{mapper[k]},{stringify_list(v, ',')},{mean:.1f}\n")
            # batch stats info
            print(f"{k},{mapper[k]}\t: {mean}")


if __name__ == "__main__":
    fire.Fire(
        {
            "stats": submission_stats,  # stats single task submission
            "stats_all": batch_stats,  # stats all tasks
        }
    )
