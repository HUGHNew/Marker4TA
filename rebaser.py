import fire


def rebase_deduction_on_roster(deduction: str, roster: str, output: str):
    """Export a deductions table with a complete list based on the list and points deducted."""
    with open(roster, encoding="utf-8-sig") as caller:
        content = caller.readlines()

    mapper = {}
    for line in content[1:]:
        sid, name = line.strip().split(",")
        mapper[sid] = name

    with open(deduction, encoding="utf-8-sig") as ded:
        content = ded.readlines()
    reasoner = {}
    header = content[0]
    for line in content[1:]:
        sid, _, reason = line.strip().split(",")
        reasoner[sid] = reason

    with open(output, "w", encoding="utf-8-sig") as writer:
        writer.write(header)
        for k in mapper:
            writer.write(f"{k},{mapper[k]},{reasoner.get(k, '')}\n")


if __name__ == "__main__":
    fire.Fire(rebase_deduction_on_roster)
