from io import TextIOWrapper
import json


def _routine_to_cron(routines: list[list[str]]):
    routines = [
        s for routine in routines for s in (routine["comments"] + [routine["command"]])
    ]


def json_to_cron(fp: TextIOWrapper):
    js = json.load(fp)

    output = js["intro"]

    if not js["routines"]:
        return output

    output.append("")  # blank line between intro and first command
    output.extend(_routine_to_cron(js["routines"]))
    output.extend(js["outro"])

    return output


if __name__ == "__main__":
    with open("src/cronk/test.json", "r") as f:
        for line in json_to_cron(f):
            print(line)
