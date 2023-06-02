from loguru import logger

from cronk.json_routine import Json, Routine


def json_to_cron(json: dict) -> list[str]:
    logger.debug(f"Converting json file to cron format")
    js = _to_Json(json)

    output = js.intro

    if not js.routines:
        return output

    output.append("")  # blank line between intro and first command
    output.extend(_routine_to_cron(js.routines))
    output.extend(js.outro)

    return output


def _routine_to_cron(routines: list[Routine]) -> list[str]:
    return [
        s
        for routine in routines
        for s in routine.comments + [routine.time + " " + routine.command]
    ]


def _to_Json(json: dict) -> Json:
    return Json(
        intro=json["intro"],
        routines=[
            Routine(comments=r["comments"], command=r["command"])
            for r in json["routines"]
        ],
        outro=json["outro"],
    )


if __name__ == "__main__":
    with open("src/cronk/test.json", "r") as f:
        for line in json_to_cron(f):
            print(line)
