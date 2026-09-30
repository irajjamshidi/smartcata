import argparse
from pathlib import Path
from promptforge.version import __version__
from promptforge.core.models import TaskIR
from promptforge.core.parser import parse
from promptforge.core.optimizer import optimize
from promptforge.core.validator import validate
from promptforge.context.scanner import inspect_project, write_context
from promptforge.handoff.package import write_package
def main(argv=None):
    parser=argparse.ArgumentParser(prog='promptforge'); sub=parser.add_subparsers(dest='command', required=True)
    for name in ('optimize','compile'):
        p=sub.add_parser(name); p.add_argument('input', nargs='?'); p.add_argument('--input', dest='input_flag'); p.add_argument('--target', default='codex')
    p=sub.add_parser('inspect'); p.add_argument('path', nargs='?', default='.')
    p=sub.add_parser('validate'); p.add_argument('input')
    sub.add_parser('version'); args=parser.parse_args(argv)
    if args.command=='version': print(__version__); return 0
    if args.command=='inspect':
        context=inspect_project(args.path); write_context(context, Path(args.path)/'.codex/task'); print(f"Inspected {context['file_count']} files; wrote .codex/task/context.*"); return 0
    if args.command=='validate':
        task=TaskIR.from_json(Path(args.input).read_text(encoding='utf-8')); result=validate(task)
        for f in result.findings: print(f'{f.severity}: {f.message}')
        return 0 if result.valid else 1
    input_path=args.input_flag or args.input
    if not input_path: parser.error('an input file is required')
    task=optimize(parse(Path(input_path).read_text(encoding='utf-8')))
    if args.command=='optimize': print(task.to_markdown()); return 0
    write_package(task, {}, '.codex/task'); print('Wrote Codex handoff to .codex/task'); return 0
if __name__=='__main__': raise SystemExit(main())
