import json
import re
from dataclasses import dataclass, field


@dataclass
class Routine:
    comments: list[str]
    time: str
    command: str

    def __init__(self, comments: list[str], command: str):
        self.comments = comments

        m = re.match(r"((?:[^ ]* ){5})(.+)", command)

        self.time = m.group(1).rstrip()
        self.command = m.group(2)


@dataclass
class Json:
    intro: list[str] = field(default_factory=list)
    routines: list[Routine] = field(default_factory=list)
    outro: list[str] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
