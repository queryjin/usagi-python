"""캐릭터 말투로 대답하는 공통 엔진."""

from __future__ import annotations

import random
import re
import unicodedata
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Expression:
    """캐릭터의 표현 하나."""

    word: str
    meanings: tuple[str, ...]
    situation: str
    loud: bool = False  # True 면 항상 "!!!" 를 붙인다 (예: 우사기의 괴성)
    echo: bool = False  # True 면 상대 말을 받아서 "<말>…라는 거야!?" 로 되묻는다 (하치와레)

    @property
    def gloss(self) -> str:
        return " / ".join(self.meanings)


def normalize(word: str) -> str:
    """번역용 비교 키: 끝의 문장부호와 공백을 뗀다."""
    return word.strip().strip("!?~♪…. ").strip()


def display_width(text: str) -> int:
    """터미널에서 차지하는 칸 수 (한글·전각 문자는 2칸)."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


@dataclass(frozen=True)
class Character:
    """대화 캐릭터 정의: 어휘, 반응 규칙, 시작 화면."""

    key: str
    name: str
    expressions: tuple[Expression, ...]
    rules: tuple[tuple[Expression, re.Pattern[str]], ...]  # 위에 있을수록 우선
    fallback: tuple[Expression, ...]
    greeting: Expression
    farewell: Expression
    small_banner: str
    art: str = ""
    draft: bool = False  # 어휘가 아직 초안인지
    profile: tuple[str, ...] = ()  # 성격·말투 요약 (/dict 에 표시)
    vocab: dict[str, Expression] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "vocab", {e.word: e for e in self.expressions})

    @property
    def title(self) -> str:
        return f"{self.name}와 대화하기  (/help 도움말, /quit 종료)"

    @property
    def art_width(self) -> int:
        return max((display_width(line) for line in self.art.splitlines()), default=0)

    def translate(self, word: str) -> str:
        key = normalize(word)
        for expression in self.expressions:
            if normalize(expression.word) == key:
                return expression.gloss
        return f"…({self.name}만 아는 말)"


@dataclass(frozen=True)
class Reply:
    expression: Expression
    text: str

    def render(self, explain: bool = False) -> str:
        if explain:
            return f"{self.text}  ({self.expression.gloss})"
        return self.text


class Chatter:
    """캐릭터 하나와 대화하는 객체. seed 를 주면 대답이 재현된다."""

    def __init__(self, character: Character, seed: int | None = None) -> None:
        self.character = character
        self._rng = random.Random(seed)

    def classify(self, message: str) -> Expression:
        """입력 문장에 맞는 표현을 고른다. 매칭이 없으면 무작위."""
        for expression, pattern in self.character.rules:
            if pattern.search(message):
                return expression
        return self._rng.choice(self.character.fallback)

    def reply(self, message: str) -> Reply:
        expression = self.classify(message)
        if expression.echo:
            return Reply(expression, self._echo(message))
        return Reply(expression, self._decorate(expression))

    def greet(self) -> Reply:
        return Reply(self.character.greeting, self._decorate(self.character.greeting))

    def farewell(self) -> Reply:
        return Reply(self.character.farewell, self._decorate(self.character.farewell))

    @staticmethod
    def _echo(message: str, limit: int = 20) -> str:
        core = re.sub(r"[\s?!.~…]+$", "", message.strip())[:limit] or "그러니까"
        return f"{core}…라는 거야!?"

    def _decorate(self, expression: Expression) -> str:
        word = expression.word
        if expression.loud:
            return f"{word}!!!"
        if word[-1] in "!?~♪…":
            return word
        bang = "!" * self._rng.randint(1, 2)
        if self._rng.random() < 0.25:
            return f"{word} {word}{bang}"
        return f"{word}{bang}"
