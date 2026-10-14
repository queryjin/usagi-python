"""터미널에서 우사기와 대화하는 CLI."""

from __future__ import annotations

import argparse
import sys
import unicodedata

from . import __version__
from .core import Usagi, translate
from .vocab import VOCAB

BANNER = r"""
   (\(\
   ( -.-)   우사기와 대화하기  (/help 도움말, /quit 종료)
   o_(")(")
"""

HELP = """\
/help       도움말
/dict       우사기 사전 보기
/explain    번역 표시 켜기/끄기
/quit       종료 (Ctrl+D 도 가능)"""


def _display_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def format_dict() -> str:
    width = max(_display_width(w) for w in VOCAB) + 2
    return "\n".join(
        f"  {e.word}{' ' * (width - _display_width(e.word))}{e.situation}" for e in VOCAB.values()
    )


def chat(usagi: Usagi, explain: bool) -> int:
    print(BANNER)
    print(f"우사기> {usagi.greet().render(explain)}")
    while True:
        try:
            message = input("나> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n우사기> {VOCAB['푸루'].word}!")
            return 0
        if not message:
            continue
        if message in ("/quit", "/exit", "/q"):
            print(f"우사기> {VOCAB['푸루'].word}!")
            return 0
        if message == "/help":
            print(HELP)
            continue
        if message == "/dict":
            print(format_dict())
            continue
        if message == "/explain":
            explain = not explain
            print(f"(번역 표시 {'ON' if explain else 'OFF'})")
            continue
        print(f"우사기> {usagi.reply(message).render(explain)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="usagi", description="치이카와 우사기와 터미널에서 대화하기")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-e", "--explain", action="store_true", help="대답 옆에 번역 표시")
    parser.add_argument("--seed", type=int, help="랜덤 시드 (재현용)")
    sub = parser.add_subparsers(dest="command")
    say_p = sub.add_parser("say", help="한 문장에 대한 대답만 출력")
    say_p.add_argument("message", nargs="+")
    tr_p = sub.add_parser("translate", help="우사기 말을 번역")
    tr_p.add_argument("word")
    sub.add_parser("dict", help="우사기 사전 출력")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    usagi = Usagi(seed=args.seed)
    if args.command == "say":
        print(usagi.reply(" ".join(args.message)).render(args.explain))
        return 0
    if args.command == "translate":
        print(translate(args.word))
        return 0
    if args.command == "dict":
        print(format_dict())
        return 0
    if not sys.stdin.isatty():
        for line in sys.stdin:
            if line.strip():
                print(usagi.reply(line.strip()).render(args.explain))
        return 0
    return chat(usagi, args.explain)
