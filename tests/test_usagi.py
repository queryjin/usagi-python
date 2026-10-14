import pytest

from usagi import VOCAB, Usagi, say, translate
from usagi.cli import main


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
def test_classify(message, expected):
    assert Usagi(seed=1).classify(message).word == expected


def test_fallback_is_known_word():
    assert Usagi(seed=1).classify("asdf").word in VOCAB


def test_reply_text_contains_word():
    reply = Usagi(seed=3).reply("배고파")
    assert "쥬르리" in reply.text
    assert "먹고 싶다" in reply.render(explain=True)


def test_seed_is_reproducible():
    a = [Usagi(seed=42).reply("asdf").text for _ in range(5)]
    b = [Usagi(seed=42).reply("asdf").text for _ in range(5)]
    assert a == b


def test_say():
    assert "우아" in say("맛있어")


@pytest.mark.parametrize("word", ["후응", "후응!!", "하아", "하아?"])
def test_translate_known(word):
    assert "…(우사기만 아는 말)" != translate(word)


def test_translate_unknown():
    assert translate("치이카와") == "…(우사기만 아는 말)"


def test_cli_say(capsys):
    assert main(["--seed", "0", "-e", "say", "배고파"]) == 0
    assert "쥬르리" in capsys.readouterr().out


def test_cli_translate(capsys):
    main(["translate", "우라"])
    assert "거대하다" in capsys.readouterr().out


def test_cli_dict(capsys):
    main(["dict"])
    out = capsys.readouterr().out
    assert all(word in out for word in VOCAB)
