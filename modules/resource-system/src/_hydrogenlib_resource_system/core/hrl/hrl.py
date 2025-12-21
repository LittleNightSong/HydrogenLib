import dataclasses
from pathlib import PurePosixPath


@dataclasses.dataclass
class HRLInfo:
    scheme: str
    path: PurePosixPath


def parse_hrl(hrl: str) -> HRLInfo:
    sep_index = hrl.find(":")
    scheme = hrl[:sep_index]
    path = hrl[sep_index + 1:]

    return HRLInfo(
        scheme,
        PurePosixPath(path)
    )
