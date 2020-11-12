from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerId:
    value: str

    def __post_init__(self):
        if len(self.value) != 36:
            raise ValueError('UUIDじゃないかもよ？')

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, string: str) -> CustomerId:
        return CustomerId(string)
