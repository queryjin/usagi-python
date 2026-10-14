"""usagi — 치이카와의 우사기처럼 대답하는 터미널 대화 라이브러리."""

from .core import Reply, Usagi, say, translate
from .vocab import VOCAB, Expression

__all__ = ["Usagi", "Reply", "Expression", "VOCAB", "say", "translate"]
__version__ = "0.1.0"
