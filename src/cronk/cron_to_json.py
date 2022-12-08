from dataclasses import dataclass, field
from io import TextIOWrapper
import re


@dataclass
class Command:
    comments: list[str] = field(default_factory=list)
    time: str = None
    command: str = None


@dataclass
class Json:
    intro: list[str] = field(default_factory=list)
    commands: list[Command] = field(default_factory=list)
    outro: list[str] = field(default_factory=list)

    def to_dict(self):
        return {"intro": self.intro, "commands": self.commands, "outro": self.outro}


def is_comment(s: str) -> bool:
    return bool(re.search("^ *#+ *", s))


def get_comment_block(file: TextIOWrapper) -> list[str]:
    pos = file.tell()
    block: list[str] = []
    while file:
        line = file.readline()

        if not is_comment(line):
            file.seek(pos)
            return block

        block.append(line)
        pos = file.tell()


def cron_to_json(file: TextIOWrapper) -> dict:
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

    pass
