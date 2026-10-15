"""터미널에서 캐릭터와 대화하는 CLI. `usagi`, `chii`, `hachi` 명령이 모두 여기로 온다."""

from __future__ import annotations

import argparse
import shutil
import sys

from . import __version__
from .characters import CHARACTERS, get_character
from .core import Character, Chatter, display_width

HELP = """\
/help         도움말
/dict         지금 캐릭터의 사전 보기
/explain      번역 표시 켜기/끄기
/char <이름>  캐릭터 바꾸기 ({names})
/quit         종료 (Ctrl+D 도 가능)""".format(names=", ".join(CHARACTERS))


def format_dict(character: Character) -> str:
    width = max(display_width(w) for w in character.vocab) + 2
    lines = [
        f"  {e.word}{' ' * (width - display_width(e.word))}{e.situation}"
        for e in character.expressions
    ]
    if character.profile:
        lines = [f"  {line}" for line in character.profile] + [""] + lines
    if character.draft:
        lines.append(f"\n  ※ {character.name} 어휘는 초안이에요. 원작 표현과 다를 수 있어요.")
    return "\n".join(lines)


def banner(character: Character, show_art: bool = True) -> str:
    """시작 화면. 아트가 없거나 터미널이 아트보다 좁으면 작은 배너로 대신한다."""
    if show_art and character.art and shutil.get_terminal_size().columns >= character.art_width:
        return f"{character.art}\n\n   {character.title}\n"
    return character.small_banner.format(title=character.title)


def chat(chatter: Chatter, explain: bool, show_art: bool = True) -> int:
    def say(text: str) -> None:
        print(f"{chatter.character.name}> {text}")

    print(banner(chatter.character, show_art))
    say(chatter.greet().render(explain))
    while True:
        try:
            message = input("나> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            say(chatter.farewell().text)
            return 0
        if not message:
            continue
        command, _, arg = message.partition(" ")
        if command in ("/quit", "/exit", "/q"):
            say(chatter.farewell().text)
            return 0
        if command == "/help":
            print(HELP)
        elif command == "/dict":
            print(format_dict(chatter.character))
        elif command == "/explain":
            explain = not explain
            print(f"(번역 표시 {'ON' if explain else 'OFF'})")
        elif command == "/char":
            key = arg.strip()
            if key not in CHARACTERS:
                print(f"(가능한 캐릭터: {', '.join(CHARACTERS)})")
                continue
            chatter = Chatter(CHARACTERS[key])
            print(banner(chatter.character, show_art))
            say(chatter.greet().render(explain))
        else:
            say(chatter.reply(message).render(explain))


def build_parser(prog: str, default_character: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog, description="치이카와 캐릭터와 터미널에서 대화하기")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "-c",
        "--char",
        choices=list(CHARACTERS),
        default=default_character,
        help=f"대화할 캐릭터 (기본: {default_character})",
    )
    parser.add_argument("-e", "--explain", action="store_true", help="대답 옆에 번역 표시")
    parser.add_argument("--seed", type=int, help="랜덤 시드 (재현용)")
    parser.add_argument("--no-art", action="store_true", help="시작할 때 아트 숨기기")
    sub = parser.add_subparsers(dest="command")
    say_p = sub.add_parser("say", help="한 문장에 대한 대답만 출력")
    say_p.add_argument("message", nargs="+")
    tr_p = sub.add_parser("translate", help="캐릭터 말을 번역")
    tr_p.add_argument("word")
    sub.add_parser("dict", help="캐릭터 사전 출력")
    sub.add_parser("art", help="캐릭터 아트 출력")
    return parser


def main(argv: list[str] | None = None, character: str = "usagi") -> int:
    args = build_parser(character, character).parse_args(argv)
    chatter = Chatter(get_character(args.char), seed=args.seed)
    selected = chatter.character
    if args.command == "say":
        print(chatter.reply(" ".join(args.message)).render(args.explain))
        return 0
    if args.command == "translate":
        print(selected.translate(args.word))
        return 0
    if args.command == "dict":
        print(format_dict(selected))
        return 0
    if args.command == "art":
        print(selected.art or selected.small_banner.format(title=selected.name))
        return 0
    if not sys.stdin.isatty():
        for line in sys.stdin:
            if line.strip():
                print(chatter.reply(line.strip()).render(args.explain))
        return 0
    return chat(chatter, args.explain, show_art=not args.no_art)


def chii_main(argv: list[str] | None = None) -> int:
    return main(argv, character="chii")


def hachi_main(argv: list[str] | None = None) -> int:
    return main(argv, character="hachi")
