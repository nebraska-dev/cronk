from dataclasses import dataclass, field
import json
import re


@dataclass
class Command:
    comments: list[str] = field(default_factory=list)
    time: str = None
    command: str = None

    def __init__(self, comments: list[str], command: str):
        self.comments = comments

        m = re.match(r"((?:[^ ]* ){5})(.*)", command)
        self.time = m.group(1).rstrip()
        self.command = m.group(2)


@dataclass
class Json:
    intro: list[str] = field(default_factory=list)
    commands: list[Command] = field(default_factory=list)
    outro: list[str] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


def _is_command(s: str) -> bool:
    return s != "" and not bool(re.search("^ *#", s))


def _split_comments(lines: list[str], command_idx: list[int]):
    end_of_intro = 0
    for i, line in enumerate(lines[: command_idx[0]]):
        if line == "":
            end_of_intro = i

    intro = lines[:end_of_intro]

    command_comments = [
        lines[(start + 1) : end]
        for start, end in zip([end_of_intro] + command_idx, command_idx + [len(lines)])
    ]

    outro = command_comments.pop()

    return intro, command_comments, outro


def cron_to_json(lines: list[str]) -> dict:
    """
    Converts a cron file to a json file.

    The json schema is:
    ```
        {
            intro: [
                "# initial comments",
                "# ..."
            ],
            commands: [
                {
                    description: [
                        "# comments above action"
                    ],
                    time: "Every day at 5 AM",
                    command: "echo Hello world"
                },
                {
                    description: [],
                    time: "Every hour",
                    command: "echo hackhackhack"
                }
            ],
            outro: [
                "# final comments",
                "..."
            ]
        }
    ```

    The intro comments and the first command's description are separated by the
    last blank line, unless there is a single comment block, in which case it is
    assumed to be the first command's description.

    ```
    # this is the intro
    # as is this

    # this is still the intro
                        <- this is the last blank line before the first command
    # this is the first command's description
    0 0 0 * * echo Hello World
    ```

    ```
    # There is no blank line, so this is all considered to be the first
    # command's description
    0 0 0 * * echo Hello World
    ```
    """

    line_types = [_is_command(line) for line in lines]

    command_idx = [i for i, line in enumerate(line_types) if line]
    commands = [lines[i] for i in command_idx]

    if not commands:  # "empty" cron file, no commands
        return Json(intro=lines)

    intro, command_comments, outro = _split_comments(lines, command_idx)

    commands = [
        Command(comment, command)
        for comment, command in zip(command_comments, commands)
    ]

    return Json(intro=intro, commands=commands, outro=outro)


if __name__ == "__main__":
    with open("src/cronk/test.txt") as f:
        lines = [s.rstrip() for s in f.readlines()]

    print(cron_to_json(lines))
