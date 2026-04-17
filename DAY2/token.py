import importlib.util
from pathlib import Path
import sysconfig


def load_stdlib_token():
    """Expose the real stdlib token module when this file is imported."""
    stdlib_token_path = Path(sysconfig.get_path("stdlib")) / "token.py"
    spec = importlib.util.spec_from_file_location("_stdlib_token", stdlib_token_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in dir(module):
        if name.startswith("__") and name not in {"__all__", "__doc__"}:
            continue
        globals()[name] = getattr(module, name)


if __name__ == "__main__":
    import nltk
    from nltk.data import find
    from nltk.tokenize import sent_tokenize, word_tokenize

    try:
        find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    try:
        find("tokenizers/punkt_tab/english")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)

    text = "Python is very powerful. It is used in NLP."

    words = word_tokenize(text)
    print("Words:", words)

    sentences = sent_tokenize(text)
    print("Sentences:", sentences)
else:
    load_stdlib_token()
