import re
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class TextStats:
    char_count: int = 0
    word_count: int = 0
    line_count: int = 0
    sentence_count: int = 0
    top_words: list[tuple[str, int]] = field(default_factory=list)


_SENTENCE_ENDINGS = re.compile(r'[.!?。！？]+')
_WORD_PATTERN = re.compile(r"[A-Za-z']+")


def analyze(text: str) -> TextStats:
    char_count = len(text)
    line_count = text.count('\n') + (1 if text and not text.endswith('\n') else 0) if text else 0
    words = _WORD_PATTERN.findall(text)
    word_count = len(words)
    sentence_count = len(_SENTENCE_ENDINGS.findall(text))

    lower_words = [w.lower() for w in words]
    top_words = Counter(lower_words).most_common(10)

    return TextStats(
        char_count=char_count,
        word_count=word_count,
        line_count=line_count,
        sentence_count=sentence_count,
        top_words=top_words,
    )


if __name__ == "__main__":
    sample = """The quick brown fox jumps over the lazy dog.
The dog barked. The fox ran away! Did the fox return? No, the fox did not.
Another sentence here. And another one! The fox is clever."""

    stats = analyze(sample)
    print(f"字符数: {stats.char_count}")
    print(f"单词数: {stats.word_count}")
    print(f"行数:   {stats.line_count}")
    print(f"句子数: {stats.sentence_count}")
    print("高频词 Top 10:")
    for word, count in stats.top_words:
        print(f"  {word}: {count}")
