from bomer import with_BOM
from grader import pre_grade
from processor import backup, submission_grades, submission_info_by_roster, submission_check
from rebaser import rebase_deduction_on_roster
from stats import batch_stats, submission_stats
from marker_common import assignment_marker

import fire

if __name__ == "__main__":
    fire.Fire(
        {
            "bom": with_BOM,
            "pregrade": pre_grade, # pregrade and log reasons
            "backup": backup, # backup submission files after check
            "diff": submission_info_by_roster,  # check submission diff with roster
            "check": submission_check,  # check submission status
            "grades": submission_grades,
            "rebase": rebase_deduction_on_roster,
            "stats_all": batch_stats,
            "stats_task": submission_stats,

            "mark": assignment_marker, # common marker
        },
        name="marker",
    )
