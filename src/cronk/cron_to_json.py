from dataclasses import dataclass
from io import TextIOWrapper
from typing import List


@dataclass
class Command:
    comments: List[str] = []
    time: str = None
    command: str = None


@dataclass
class Json:
    intro: List[str] = []
    commands: List[Command] = []
    outro: List[str] = []


def cron_to_json(file: TextIOWrapper):
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
