"""우사기(치이카와)의 어휘 사전."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    """우사기의 표현 하나."""

    word: str
    meanings: tuple[str, ...]
    situation: str

    @property
    def gloss(self) -> str:
        return " / ".join(self.meanings)


YAHA = Expression("야하", ("찾았다!", "등장!"), "뭔가를 찾았을 때, 혹은 등장할 때")
URA = Expression("우라", ("최근", "거대하다"), "최근 / 거대하다 (상황에 따라 다름)")
PURUYA = Expression("푸루야", ("같이 하자!", "따라와!", "힘내!"), "공감 요구, 따라오라는 초대, 응원")
PURU = Expression("푸루", ("알겠어", "잡초 이름"), "잡초 이름, 알겠어")
HAA = Expression("하아?", ("뭐야?", "놀랐어!", "어이없네"), "뭐야?, 놀랐을 때, 어이없을 때")
HUNG = Expression("후응", ("맞아",), "맞아 (긍정의 의미)")
JURURI = Expression("쥬르리", ("먹고 싶다…",), "식욕이 돌 때")
MIYAAA = Expression("미야아아", ("어서 오세요",), "어서 오세요")
UA = Expression("우아", ("맛있다",), "맛있다")
PURUYA_URAURA = Expression("푸루야우라우라", ("해독 불가능한 기괴한 괴성",), "해독 불가능한 기괴한 괴성")

VOCAB: dict[str, Expression] = {
    e.word: e
    for e in (YAHA, URA, PURUYA, PURU, HAA, HUNG, JURURI, MIYAAA, UA, PURUYA_URAURA)
}
