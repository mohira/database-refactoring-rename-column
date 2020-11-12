from dataclasses import dataclass


@dataclass(frozen=True)
class FName:
    value: str

    def __post_init__(self):
        if not (1 <= len(self.value) <= 40):
            raise ValueError('1文字以上40文字以下でよろしくな！')
