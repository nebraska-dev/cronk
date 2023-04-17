import json

from loguru import logger

from cronk.json_routine import Json, Routine


def json_to_cron(text: str) -> list[str]:
    logger.debug(f"Converting json file to cron format")
    js = _to_Json(json.loads(text))

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
