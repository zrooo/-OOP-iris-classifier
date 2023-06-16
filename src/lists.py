from __future__ import annotations
import string

CHARACTERS = list(string.ascii_letters) + [" "]


def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [(letter, count) for letter, count in frequencies if count > 0]
    return non_zero


from typing import Optional, cast, Any
from dataclasses import dataclass
import datetime
from datetime import timezone


@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def __lt__(self, other: Any) -> bool:
        if self.data_source == "Local":
            self_datetime = datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            self_datetime = datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)
        if other.data_source == "Local":
            other_datetime = datetime.datetime.fromtimestamp(
                cast(float, other.timestamp), tz=timezone.utc
            )
        else:
            other_datetime = datetime.datetime.fromisoformat(
                cast(str, other.creation_date)
            ).replace(tzinfo=timezone.utc)
        return self_datetime < other_datetime

    def __eq__(self, other: object) -> bool:
        return self.datetime == cast(MultiItem, other).datetime

    @property
    def datetime(self) -> datetime.datetime:
        if self.data_source == "Local":
            return datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            return datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)



from functools import total_ordering


@total_ordering
class MultiItemTO(MultiItem):
    pass



@dataclass(frozen=True)
class SimpleMultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str


def by_timestamp(item: SimpleMultiItem) -> datetime.datetime:
    if item.data_source == "Local":
        return datetime.datetime.fromtimestamp(
            cast(float, item.timestamp), tz=timezone.utc
        )
    elif item.data_source == "Remote":
        return datetime.datetime.fromisoformat(cast(str, item.creation_date)).replace(
            tzinfo=timezone.utc
        )
    else:
        raise ValueError(f"Unknown data_source in {item!r}")



class LocalItem:
    data_source: str
    timestamp: float
    name: str
    owner_etc: str

    def __repr__(self) -> str:
        return f"LocalItem(timestamp={self.timestamp})"


class RemoteItem:
    data_souce: str
    creation_date: str
    name: str
    owner_etc: str

    def __repr__(self) -> str:
        return f"RemoteItem(creation_date={self.creation_date})"

