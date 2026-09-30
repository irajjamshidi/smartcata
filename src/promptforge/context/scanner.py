from __future__ import annotations
import json
from pathlib import Path
SIGNALS = ("README", "pyproject.toml", "package.json", "requirements.txt", "Dockerfile")
def inspect_project(path: str | Path) -> dict:
    root=Path(path).resolve(); files=[]
    for p in root.rglob("*"):
        if ".git" in p.parts or p.is_dir(): continue
        rel=str(p.relative_to(root))
        if len(files) < 300: files.append(rel)
    top=[f for f in files if Path(f).name in SIGNALS]
    dirs=sorted({str(Path(f).parent) for f in files if str(Path(f).parent) != "."})
    indicators=[]
    names={Path(f).name for f in files}
    if "pyproject.toml" in names: indicators.append("Python project")
    if "package.json" in names: indicators.append("Node.js project")
    if any("fastapi" in f.casefold() for f in files): indicators.append("FastAPI-related files")
    return {"root":str(root), "important_files":top, "source_directories":[d for d in dirs if "src" in d or "backend" in d], "test_directories":[d for d in dirs if "test" in d], "framework_indicators":indicators, "file_count":len(files), "files":files}
def write_context(context: dict, output: str | Path) -> tuple[Path, Path]:
    output=Path(output); output.mkdir(parents=True, exist_ok=True)
    js=output/'context.json'; md=output/'context.md'; js.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding='utf-8')
    md.write_text("# Project Context\n\n"+"\n".join(f"- **{k.replace('_',' ')}:** {v}" for k,v in context.items() if k != 'files'), encoding='utf-8')
    return md,js
