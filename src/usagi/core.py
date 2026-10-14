"""사용자 입력을 우사기 언어로 응답하는 엔진."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass

from .vocab import (
    HAA,
    HUNG,
    JURURI,
    MIYAAA,
    PURU,
    PURUYA,
    PURUYA_URAURA,
    UA,
    URA,
    VOCAB,
    YAHA,
    Expression,
)

# (표현, 키워드 패턴) — 위에 있을수록 우선순위가 높다.
RULES: list[tuple[Expression, re.Pattern[str]]] = [
    (PURUYA_URAURA, re.compile(r"ㅋㅋㅋㅋ|ㅎㅎㅎㅎ|!!!|미쳤|미친|대박|난리|으아아|crazy|wtf|lol", re.I)),
    (UA, re.compile(r"맛있|맛나|꿀맛|존맛|yummy|delicious|tasty", re.I)),
    (JURURI, re.compile(r"배고|배가 고|먹고 ?싶|먹을래|밥|간식|라면|고기|푸딩|hungry|food|\beat\b", re.I)),
    (MIYAAA, re.compile(r"다녀왔|왔어|왔다|들어왔|도착|퇴근|i'?m home|i'?m back", re.I)),
    (YAHA, re.compile(r"안녕|하이|ㅎㅇ|찾았|발견|짠|등장|hello|\bhi\b|\bhey\b|found", re.I)),
    (URA, re.compile(r"최근|요즘|요새|크다|거대|엄청|big|huge|recent|lately", re.I)),
    (PURUYA, re.compile(r"힘들|피곤|지쳤|우울|슬퍼|화이팅|파이팅|응원|같이|가자|하자|할까|tired|sad|let'?s", re.I)),
    (HUNG, re.compile(r"맞지|그치|그렇지|맞아|그래\?|인정|좋아\?|right\?|yes|yeah", re.I)),
    (PURU, re.compile(r"해줘|해 줘|부탁|알았|알겠|ㅇㅋ|오케이|please|\bok\b|okay", re.I)),
    (HAA, re.compile(r"\?|뭐|왜|진짜|헐|어떻게|what|why|huh", re.I)),
]

FALLBACK: tuple[Expression, ...] = (HAA, PURU, HUNG, URA, PURUYA, YAHA)


@dataclass(frozen=True)
class Reply:
    expression: Expression
    text: str

    def render(self, explain: bool = False) -> str:
        if explain:
            return f"{self.text}  ({self.expression.gloss})"
        return self.text


class Usagi:
    """우사기와 대화하는 객체.

    >>> u = Usagi(seed=0)
    >>> u.reply("배고파").expression.word
    '쥬르리'
    """

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def classify(self, message: str) -> Expression:
        """입력 문장에 맞는 우사기 표현을 고른다. 매칭이 없으면 무작위."""
        for expression, pattern in RULES:
            if pattern.search(message):
                return expression
        return self._rng.choice(FALLBACK)

    def reply(self, message: str) -> Reply:
        expression = self.classify(message)
        return Reply(expression, self._decorate(expression))

    def greet(self) -> Reply:
        """등장 인사."""
        return Reply(YAHA, self._decorate(YAHA))

    def _decorate(self, expression: Expression) -> str:
        word = expression.word
        if word.endswith("?"):
            return word
        if expression is PURUYA_URAURA:
            return f"{word}!!!"
        bang = "!" * self._rng.randint(1, 2)
        if self._rng.random() < 0.25:
            return f"{word} {word}{bang}"
        return f"{word}{bang}"


_default = Usagi()


def say(message: str, explain: bool = False) -> str:
    """한 줄 입력에 대한 우사기의 대답을 문자열로 돌려준다."""
    return _default.reply(message).render(explain=explain)


def translate(word: str) -> str:
    """우사기 표현을 사람 말로 번역한다."""
    key = word.strip().rstrip("!").strip()
    expression = VOCAB.get(key) or VOCAB.get(key + "?") or VOCAB.get(key.rstrip("?"))
    if expression is None:
        return "…(우사기만 아는 말)"
    return expression.gloss
