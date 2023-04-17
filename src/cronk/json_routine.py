import json
import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Routine:
    comments: List[str]
    time: str
    command: str

    def __init__(self, comments: List[str], command: str):
        self.comments = comments

        m = re.match(r"((?:[^ ]* ){5})(.+)", command)

        self.time = m.group(1).rstrip()
        self.command = m.group(2)


@dataclass
class Json:
    intro: List[str] = field(default_factory=list)
    routines: List[Routine] = field(default_factory=list)
    outro: List[str] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
