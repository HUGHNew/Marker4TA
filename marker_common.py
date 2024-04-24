import os
import os.path as osp
from logger import get_default_logger

from marker_base import mark_task

logger = get_default_logger()

def assignment_marker(
    src_dir: str,
    tgt_pre: str = "dist",
    *,
    tmp_file: str = "tmp.pdf",
    reason_limit: int = 0,
    deduction: str = "deduction.csv",
):
    """
    Assignments marker for standardized daily submissions.
    """
    assert osp.exists(src_dir)
    tgt_dir = osp.join(tgt_pre, src_dir)
    if not osp.exists(tgt_dir):
        os.mkdir(tgt_dir)

    logger.info(f"Marking assignments in {src_dir}")
    if reason_limit > 0:
        logger.info(f"Limit for score reason: {reason_limit}")
        reasons = {}
        with open(osp.join(src_dir, deduction)) as fd:
            lines = fd.read().splitlines()[1:]
        for line in lines:
            sid, name, reason = line.split(",")
            reasons[sid] = reason  # .replace('，','\n')
    for f in os.listdir(src_dir):
        if f.endswith(".csv"):
            continue
        if not f.endswith(".pdf"):
            logger.info(f"{src_dir}/{f} needs manual marking")
            continue
        src = osp.join(src_dir, f)
        tgt = osp.join(tgt_dir, f)
        sid, _, _, content = osp.basename(src).split(".")[-2].split("-")  # get score from file name
        # reason for low score
        extra = None
        try:
            score = int(content)
            if score < reason_limit:
                assert sid in reasons, f"{sid} not found in {src_dir}"
                extra = reasons[sid].replace(")，", ")\n")
        except ValueError:
            logger.error(f"unexpected score: {content} when processing {src}")
            continue

        mark_task(src, content, tmp_file, tgt, extra)
