"""등록된 캐릭터 목록."""

from __future__ import annotations

from ..core import Character
from .chii import CHII
from .hachi import HACHI
from .usagi import USAGI, Usagi

CHARACTERS: dict[str, Character] = {c.key: c for c in (USAGI, CHII, HACHI)}


def get_character(key: str) -> Character:
    try:
        return CHARACTERS[key]
    except KeyError:
        raise ValueError(f"모르는 캐릭터: {key!r} (가능: {', '.join(CHARACTERS)})") from None


__all__ = ["CHARACTERS", "CHII", "HACHI", "USAGI", "Usagi", "get_character"]
