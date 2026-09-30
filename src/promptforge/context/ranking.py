from pathlib import Path
def rank_files(files: list[str], task_text: str) -> list[str]:
    words={w.casefold() for w in task_text.replace("/", " ").split() if len(w)>2}
    return sorted(files, key=lambda f: (-sum(w in f.casefold() for w in words), f))
