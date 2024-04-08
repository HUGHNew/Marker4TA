from bomer import with_BOM
from grader import pre_grade
from processor import backup, submission_grades
from rebaser import rebase_deduction_on_roster
from stats import batch_stats, submission_stats

import fire

if __name__ == "__main__":
    fire.Fire(
        {
            "bom": with_BOM,
            "pregrade": pre_grade,
            "backup": backup,
            "grades": submission_grades,
            "rebase": rebase_deduction_on_roster,
            "stats_all": batch_stats,
            "stats_task": submission_stats,
        },
        name="marker",
    )
