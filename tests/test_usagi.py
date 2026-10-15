import os

import pytest

from usagi import CHARACTERS, VOCAB, Chatter, Usagi, get_character, say, translate
from usagi import cli
from usagi.cli import chii_main, hachi_main, main


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("안녕!", "야하"),
        ("열쇠 찾았다", "야하"),
        ("요즘 어때", "우라"),
        ("오늘 너무 힘들어", "푸루야"),
        ("이거 해줘", "푸루"),
        ("그게 뭔데?", "하아?"),
        ("이거 맞지", "후응"),
        ("배고파", "쥬르리"),
        ("다녀왔어", "미야아아"),
        ("이 푸딩 진짜 맛있다", "우아"),
        ("ㅋㅋㅋㅋㅋ 미쳤다", "푸루야우라우라"),
    ],
)
def test_usagi_classify(message, expected):
    assert Usagi(seed=1).classify(message).word == expected


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("토벌 가자", "야앗!!"),
        ("벌레 나왔어", "이얏!"),
        ("그거 싫어", "야다앗!"),
        ("너무 슬퍼", "와아…"),
        ("우와 예쁘다", "와아…"),
        ("배고파", "후!"),
        ("헉 깜짝이야", "왓"),
        ("같이 할래?", "응"),
    ],
)
def test_chii_classify(message, expected):
    assert Chatter(get_character("chii"), seed=1).classify(message).word == expected


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("울고 있어", "울어버렸다…"),
        ("오늘 비 와서 최악", "기쁨이 없어~"),
        ("폰 떨어뜨렸어", "큰일이다! 위험해!"),
        ("내일 시험 걱정돼", "어떻게든 되라앗!"),
        ("도전해볼까", "안 될 것 같으면 그만두면 되지!"),
        ("빨리 해야 돼", "서두르지 않아도 괜찮아~"),
        ("오늘 힘들다", "괜찮아! 괜찮아!"),
        ("사진 찍었는데", "한 장이라도 좋은 게 있으면 됐지!"),
        ("안녕", "안녕~!"),
        ("합격했어", "기쁘다! 와!"),
        ("내일 쉬는 날이래", "…라는 거야!?"),
    ],
)
def test_hachi_classify(message, expected):
    assert Chatter(get_character("hachi"), seed=1).classify(message).word == expected


def test_hachi_echoes_message():
    reply = Chatter(get_character("hachi")).reply("내일 쉬는 날이래?!")
    assert reply.text == "내일 쉬는 날이래…라는 거야!?"


@pytest.mark.parametrize("key", list(CHARACTERS))
def test_every_character_is_consistent(key):
    character = CHARACTERS[key]
    words = set(character.vocab)
    assert {e.word for e, _ in character.rules} <= words
    assert set(e.word for e in character.fallback) <= words
    assert character.greeting.word in words and character.farewell.word in words
    assert "{title}" in character.small_banner
    for _ in range(20):
        assert Chatter(character).classify("zzz").word in words


def test_unknown_character():
    with pytest.raises(ValueError):
        get_character("momonga")


def test_reply_text_contains_word():
    reply = Usagi(seed=3).reply("배고파")
    assert "쥬르리" in reply.text
    assert "먹고 싶다" in reply.render(explain=True)


def test_hachi_phrases_are_not_decorated():  # 이미 문장부호로 끝나면 꾸미지 않는다
    assert Chatter(get_character("hachi"), seed=1).reply("안녕").text == "안녕~!"


def test_seed_is_reproducible():
    a = [Usagi(seed=42).reply("asdf").text for _ in range(5)]
    b = [Usagi(seed=42).reply("asdf").text for _ in range(5)]
    assert a == b


def test_say():
    assert "우아" in say("맛있어")
    assert "기쁘다" in say("맛있다", character="hachi")


@pytest.mark.parametrize("word", ["후응", "후응!!", "하아", "하아?"])
def test_translate_known(word):
    assert translate(word) != "…(우사기만 아는 말)"


def test_translate_other_characters():
    assert translate("어떻게든 되라앗", character="hachi") == "될 대로 되라! / 그래도 해보자"
    assert translate("라는 거야", character="hachi") == "…라는 거야!?"
    assert translate("이얏", character="chii") == "싫어! / 무서워!"


def test_translate_unknown():
    assert translate("치이카와") == "…(우사기만 아는 말)"


def test_vocab_is_usagi():
    assert "푸루야" in VOCAB


def test_cli_say(capsys):
    assert main(["--seed", "0", "-e", "say", "배고파"]) == 0
    assert "쥬르리" in capsys.readouterr().out


def test_cli_char_option_and_entry_points(capsys):
    main(["-c", "hachi", "say", "맛있다"])
    chii_main(["say", "배고파"])
    hachi_main(["translate", "괜찮아! 괜찮아!"])
    out = capsys.readouterr().out
    assert "기쁘다! 와!" in out and "후!" in out and "위로" in out


def test_cli_translate(capsys):
    main(["translate", "우라"])
    assert "거대하다" in capsys.readouterr().out


@pytest.mark.parametrize("key", list(CHARACTERS))
def test_cli_dict(capsys, key):
    main(["-c", key, "dict"])
    out = capsys.readouterr().out
    assert all(word in out for word in CHARACTERS[key].vocab)


def test_cli_art(capsys):
    main(["art"])
    assert CHARACTERS["usagi"].art in capsys.readouterr().out


def test_usagi_art_is_small():
    usagi = CHARACTERS["usagi"]
    assert usagi.art_width <= 40
    assert len(usagi.art.splitlines()) <= 25


def test_banner(monkeypatch):
    usagi, chii = CHARACTERS["usagi"], CHARACTERS["chii"]
    small = usagi.small_banner.format(title=usagi.title)
    monkeypatch.setattr(cli.shutil, "get_terminal_size", lambda: os.terminal_size((20, 20)))
    assert cli.banner(usagi) == small
    monkeypatch.setattr(cli.shutil, "get_terminal_size", lambda: os.terminal_size((120, 40)))
    assert usagi.art in cli.banner(usagi)
    assert cli.banner(usagi, show_art=False) == small
    assert cli.banner(chii) == chii.small_banner.format(title=chii.title)
