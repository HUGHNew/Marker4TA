# Task marker for TA

Default encoding should be UTF-8, but here use UTF-8 with BOM for XLSX compatibility.

files Functionality
- cli.py: command line interface all in one
- bomer.py: make file's encoding into UTF-8with BOM
- grader.py: pregrade the submissions (You may modify it for your own grading policy)
- process.py:
  - backup submission files
  - record submission scores
- rebaser.py: log the deduction info based on the roster
- stats.py: generate statistics report based on the submission scores

some default files will be generated in the task directory:
- provider.csv: sid,name (records who submits the assignment)
- submission.csv: sid,ext,filename (records the submission files)
- deduction.csv: sid,name,deduction,dedut_score (records the deductions for each submission)
- grade.csv: sid,name,score (records the final scores for each submission)

> Thanks to [reportlab](https://docs.reportlab.com/install/open_source_installation/) and [pypdf](https://github.com/py-pdf/pypdf) for providing fantastic PDF operations.