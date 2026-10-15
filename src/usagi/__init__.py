"""usagi — 치이카와 캐릭터(우사기, 치이카와, 하치와레)처럼 대답하는 터미널 대화 라이브러리."""

from __future__ import annotations

from .characters import CHARACTERS, CHII, HACHI, USAGI, Usagi, get_character
from .core import Character, Chatter, Expression, Reply

VOCAB = USAGI.vocab  # 0.1.0 호환용: 우사기 사전

__all__ = [
    "CHARACTERS",
    "CHII",
    "HACHI",
    "USAGI",
    "VOCAB",
    "Character",
    "Chatter",
    "Expression",
    "Reply",
    "Usagi",
    "get_character",
    "say",
    "translate",
]
__version__ = "0.2.0"

_chatters: dict[str, Chatter] = {}


def say(message: str, explain: bool = False, character: str = "usagi") -> str:
    """한 줄 입력에 대한 캐릭터의 대답을 문자열로 돌려준다."""
    if character not in _chatters:
        _chatters[character] = Chatter(get_character(character))
    return _chatters[character].reply(message).render(explain=explain)


def translate(word: str, character: str = "usagi") -> str:
    """캐릭터의 말을 사람 말로 번역한다."""
    return get_character(character).translate(word)
